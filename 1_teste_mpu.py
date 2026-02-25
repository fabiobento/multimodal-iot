# Leitura de dados do MPU6050 com o Raspberry Pi
import smbus
import time

# Endereços de registradores do MPU6050
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H  = 0x43
DEVICE_ADDR  = 0x68  # Endereço I2C padrão do MPU6050

def MPU_Init():
    """
    Inicializa o sensor MPU6050 configurando a taxa de amostragem, 
    gerenciamento de energia, configuração do giroscópio e interrupções.
    """
    bus.write_byte_data(DEVICE_ADDR, SMPLRT_DIV, 7)
    bus.write_byte_data(DEVICE_ADDR, PWR_MGMT_1, 1)
    bus.write_byte_data(DEVICE_ADDR, CONFIG, 0)
    bus.write_byte_data(DEVICE_ADDR, GYRO_CONFIG, 24)
    bus.write_byte_data(DEVICE_ADDR, INT_ENABLE, 1)

def read_raw_data(addr):
    """
    Lê dados brutos de 16 bits de um endereço específico do sensor.
    
    Args:
        addr: O endereço do registrador de início (High byte).
        
    Returns:
        O valor inteiro de 16 bits com sinal.
    """
    # Lê dois bytes (High e Low) e os concatena
    high = bus.read_byte_data(DEVICE_ADDR, addr)
    low = bus.read_byte_data(DEVICE_ADDR, addr+1)
    
    value = ((high << 8) | low)
    
    # Converte o valor para um inteiro com sinal (complemento de 2)
    if(value > 32768):
        value = value - 65536
    return value

# Inicializa o barramento I2C (1 para Raspberry Pi 2/3/4/5)
bus = smbus.SMBus(1)
MPU_Init()

print("Lendo dados do MPU6050...")

try:
    while True:
        # Lê os dados brutos do Acelerômetro (X, Y, Z)
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_XOUT_H+2)
        acc_z = read_raw_data(ACCEL_XOUT_H+4)
        
        # Lê os dados brutos do Giroscópio (X, Y, Z)
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_XOUT_H+2)
        gyro_z = read_raw_data(GYRO_XOUT_H+4)
        
        # Converte valores brutos para unidades físicas (g e °/s)
        # Divisores baseados na configuração padrão do datasheet
        Ax = acc_x/16384.0
        Ay = acc_y/16384.0
        Az = acc_z/16384.0
        
        Gx = gyro_x/131.0
        Gy = gyro_y/131.0
        Gz = gyro_z/131.0
        
        # Exibe os resultados formatados
        print(f"Ax={Ax:.2f} g Ay={Ay:.2f} g Az={Az:.2f} g | Gx={Gx:.2f}°/s Gy={Gy:.2f}°/s Gz={Gz:.2f}°/s")
        
        # Intervalo entre leituras
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nLeitura interrompida pelo usuário. Parando...")