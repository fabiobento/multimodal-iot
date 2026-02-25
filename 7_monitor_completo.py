import time
import smbus
import bme680
from PIL import ImageFont

# --- NOVAS IMPORTAÇÕES PARA O DISPLAY (LUMA) ---
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

# --- 1. CONFIGURAÇÃO DO DISPLAY OLED (SH1106) ---
# Substituímos a configuração do Adafruit pela do Luma
try:
    # Cria a interface I2C para o display
    serial = i2c(port=1, address=0x3C)
    # Inicializa o driver SH1106
    device = sh1106(serial)
    print("OLED (SH1106): OK")
except Exception as e:
    print(f"Erro OLED: {e}")
    # Se der erro no display, o script continua para mostrar dados no terminal?
    # Vamos deixar continuar, mas device ficará indefinido. 
    # Idealmente tratamos isso, mas para teste vamos seguir.

# Carrega a fonte (Mesma lógica anterior)
try:
    font = ImageFont.truetype("DejaVuSans.ttf", 10)
except IOError:
    font = ImageFont.load_default()

# --- 2. CONFIGURAÇÃO DO BME680 (0x77) ---
try:
    # Tenta endereço secundário (0x77)
    sensor_bme = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
except (RuntimeError, IOError):
    try:
        # Se falhar, tenta o primário (0x76)
        sensor_bme = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
    except Exception as e:
        print(f"Erro BME680: {e}")

# Configurações de leitura do BME
if 'sensor_bme' in locals():
    sensor_bme.set_humidity_oversample(bme680.OS_2X)
    sensor_bme.set_pressure_oversample(bme680.OS_4X)
    sensor_bme.set_temperature_oversample(bme680.OS_8X)
    sensor_bme.set_filter(bme680.FILTER_SIZE_3)
    sensor_bme.set_gas_status(bme680.ENABLE_GAS_MEAS)
    sensor_bme.set_gas_heater_temperature(320)
    sensor_bme.set_gas_heater_duration(150)
    sensor_bme.select_gas_heater_profile(0)
    print("BME680: OK (Configurado)")

# --- 3. CONFIGURAÇÃO DO MPU6050 (0x68) ---
MPU_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
bus = smbus.SMBus(1)

def mpu_init():
    try:
        bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0)
        print("MPU6050: OK (0x68)")
    except Exception as e:
        print(f"Erro MPU6050: {e}")

def read_raw_mpu(addr):
    try:
        high = bus.read_byte_data(MPU_ADDR, addr)
        low = bus.read_byte_data(MPU_ADDR, addr+1)
        value = ((high << 8) | low)
        if(value > 32768): value = value - 65536
        return value
    except:
        return 0 # Retorna 0 se falhar a leitura

mpu_init()

# --- LOOP PRINCIPAL ---
print("\nIniciando monitoramento... Pressione Ctrl+C para sair.")

try:
    while True:
        # A. Ler BME680
        temp_str = "--.-C"
        gas_str = "Wait"
        
        if 'sensor_bme' in locals() and sensor_bme.get_sensor_data():
            temp_str = f"{sensor_bme.data.temperature:.1f}C"
            if sensor_bme.data.heat_stable:
                gas_str = f"{sensor_bme.data.gas_resistance / 1000:.1f}K"
            else:
                gas_str = "Heat"

        # B. Ler MPU6050 (Eixo X)
        acc_x = read_raw_mpu(ACCEL_XOUT_H) / 16384.0
        vib_str = f"{acc_x:.2f}g"

        # C. Atualizar Display OLED (Usando Luma Canvas)
        # O 'with canvas(device)' cria o desenho e envia para tela automaticamente ao sair do bloco
        with canvas(device) as draw:
            # Não precisa limpar a tela (fill 0), o canvas já faz isso a cada frame
            
            draw.text((0, 0),  f"Temp: {temp_str}", font=font, fill="white")
            draw.text((0, 12), f"Gas : {gas_str}", font=font, fill="white")
            draw.text((0, 24), f"Vib X: {vib_str}", font=font, fill="white")
            
            # Linha divisória estética
            draw.line((0, 40, 128, 40), fill="white")
            draw.text((0, 45), "Status: ON", font=font, fill="white")

        # D. Print no terminal
        print(f"T: {temp_str} | G: {gas_str} | Vib: {vib_str}")
        
        # Pausa para não sobrecarregar a CPU e facilitar leitura
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nEncerrado.")