import time
import threading
import smbus
import bme680
import pyaudio
import audioop
import math
from ctypes import *
from contextlib import contextmanager
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageFont

# --- SILENCIADOR ALSA ---
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt): pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
@contextmanager
def no_alsa_error():
    try:
        asound = cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(c_error_handler)
        yield
        asound.snd_lib_error_set_handler(None)
    except:
        yield

# --- DADOS GLOBAIS ---
# Armazena os valores numéricos brutos para envio
data_packet = {
    "temp": 0.0,
    "gas_res": 0.0,
    "vib_x": 0.0,
    "audio_db": 0.0
}

# --- CONFIGURAÇÃO AUDIO ---
def audio_thread_func():
    CHUNK = 4096 
    FORMAT = pyaudio.paInt32
    CHANNELS = 2
    RATE = 48000
    
    with no_alsa_error():
        p = pyaudio.PyAudio()
    
    dev_index = 0
    for i in range(p.get_device_count()):
        if "google" in p.get_device_info_by_index(i).get('name').lower():
            dev_index = i
            break
            
    try:
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                        input=True, input_device_index=dev_index, 
                        frames_per_buffer=CHUNK)
        
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            rms = audioop.rms(data, 4)
            if rms > 0:
                db = 20 * math.log10(rms)
                # SEU AJUSTE DE CALIBRAÇÃO AQUI
                clean_db = max(0, int(db - 120)) 
                data_packet["audio_db"] = clean_db
            else:
                data_packet["audio_db"] = 0
    except:
        pass

# --- CONFIGURAÇÃO SENSORES I2C ---
# MPU6050
MPU_ADDR = 0x68
bus = smbus.SMBus(1)
try:
    bus.write_byte_data(MPU_ADDR, 0x6B, 0)
except: pass

def read_mpu_raw():
    try:
        high = bus.read_byte_data(MPU_ADDR, 0x3B)
        low = bus.read_byte_data(MPU_ADDR, 0x3B+1)
        value = ((high << 8) | low)
        if(value > 32768): value = value - 65536
        return value / 16384.0
    except:
        return 0.0

# BME680
try:
    sensor_bme = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
except:
    try: sensor_bme = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
    except: sensor_bme = None

if sensor_bme:
    sensor_bme.set_gas_status(bme680.ENABLE_GAS_MEAS)
    sensor_bme.set_gas_heater_temperature(320)
    sensor_bme.set_gas_heater_duration(150)
    sensor_bme.select_gas_heater_profile(0)

# OLED
try:
    oled = sh1106(i2c(port=1, address=0x3C))
except: pass
try: font = ImageFont.truetype("DejaVuSans.ttf", 10)
except: font = ImageFont.load_default()

# --- START ---
audio_t = threading.Thread(target=audio_thread_func)
audio_t.daemon = True 
audio_t.start()

# Aguarda sensores estabilizarem
time.sleep(2)

# Frequência de Coleta (Hz)
# O Edge Impulse gosta de frequências estáveis. 
# 50Hz (0.02s) é bom para vibração mecânica de impressora.
FREQUENCY = 50 
INTERVAL = 1.0 / FREQUENCY

try:
    while True:
        start_time = time.time()
        
        # 1. Ler Sensores
        vib = read_mpu_raw()
        data_packet["vib_x"] = vib
        
        if sensor_bme and sensor_bme.get_sensor_data():
            data_packet["temp"] = sensor_bme.data.temperature
            if sensor_bme.data.heat_stable:
                data_packet["gas_res"] = sensor_bme.data.gas_resistance
            
        # 2. SAÍDA DE DADOS (CRUCIAL PARA O EDGE IMPULSE)
        # Formato CSV: temperatura, gas, vibração, audio_db
        print(f"{data_packet['temp']:.2f},{data_packet['gas_res']:.2f},{data_packet['vib_x']:.4f},{data_packet['audio_db']:.2f}", flush=True)

        # 3. Atualizar OLED (Opcional - Pode comentar se quiser mais velocidade)
        # Atualizamos o OLED menos vezes para não engasgar o print de dados
        # Usamos um contador simples ou verificamos tempo, mas aqui vai simplificado:
        # (Se sentir que o CSV está lento, comente o bloco 'with canvas' abaixo)
        
        # with canvas(oled) as draw:
        #     draw.text((0, 0), "COLETANDO DADOS...", font=font, fill="white")
        #     draw.text((0, 20), f"Vib: {vib:.2f}", font=font, fill="white")
        #     draw.text((0, 35), f"dB: {data_packet['audio_db']}", font=font, fill="white")

        # Controle de Frequência
        elapsed = time.time() - start_time
        sleep_time = INTERVAL - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

except KeyboardInterrupt:
    pass