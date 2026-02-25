import time
import threading
import smbus
import bme680
import pyaudio
import audioop
import math
import requests
import json
import os
from ctypes import *
from contextlib import contextmanager
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageFont

# --- CONFIGURAÇÕES DO USUÁRIO ---
EI_API_KEY = "ei_43b3dbe4b65e6887830799c9cd6cab7ef1c219fbb4b5ead24656cfbba49a8926"  # <--- COLAR SUA CHAVE AQUI
DEVICE_NAME = "RaspberryPi-Zero2W"
SAMPLE_TIME_SEC = 10 
FREQUENCY_HZ = 50    
LABEL_PADRAO = "normal" 

# --- URL DA API DE INGESTÃO ---
INGESTION_URL = "https://ingestion.edgeimpulse.com/api/training/data"

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

# --- VARIÁVEIS GLOBAIS ---
current_audio_db = 0.0

# --- THREAD DE ÁUDIO (Modo PulseAudio) ---
def audio_thread_func():
    global current_audio_db
    CHUNK = 4096 
    FORMAT = pyaudio.paInt32
    RATE = 44100 # Taxa padrão mais compatível com PulseAudio
    
    with no_alsa_error():
        p = pyaudio.PyAudio()
    
    # ESTRATÉGIA: Tentar usar o dispositivo 'default' (Index 9 no seu scan)
    # pois ele reportou ter canais disponíveis.
    target_index = -1
    
    # 1. Procura pelo dispositivo 'default'
    for i in range(p.get_device_count()):
        try:
            info = p.get_device_info_by_index(i)
            if "default" in info.get('name').lower():
                target_index = i
                print(f"[AUDIO] Usando dispositivo do sistema: {info.get('name')}")
                break
        except: pass
            
    # Se não achar default, tenta o google
    if target_index == -1:
         for i in range(p.get_device_count()):
            if "google" in p.get_device_info_by_index(i).get('name').lower():
                target_index = i
                print(f"[AUDIO] Tentando hardware direto: {info.get('name')}")
                break

    # 2. Tentar abrir o stream (Mono é mais seguro via Pulse)
    stream = None
    try:
        # Tentativa 1: Mono (1 canal) no dispositivo default
        stream = p.open(format=FORMAT, channels=1, rate=RATE, 
                        input=True, input_device_index=target_index, 
                        frames_per_buffer=CHUNK)
        print(f"[AUDIO] Sucesso iniciando em MONO!")
    except Exception as e:
        print(f"[AUDIO] Falha em Mono: {e}")
        try:
            # Tentativa 2: Stereo (2 canais)
            stream = p.open(format=FORMAT, channels=2, rate=RATE, 
                            input=True, input_device_index=target_index, 
                            frames_per_buffer=CHUNK)
            print(f"[AUDIO] Sucesso iniciando em STEREO!")
        except Exception as e2:
            print(f"[AUDIO] Falha em Stereo: {e2}")

    
    if stream is None:
        print("[AUDIO] ERRO FATAL: Microfone inacessível. Tente reiniciar (sudo reboot).")
        return

    # 3. Loop de Leitura
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            rms = audioop.rms(data, 4)
            if rms > 0:
                db = 20 * math.log10(rms)
                current_audio_db = max(0, int(db - 120)) 
            else:
                current_audio_db = 0
    except Exception as e:
        print(f"[AUDIO] Erro leitura: {e}")

# --- CONFIGURAÇÃO SENSORES I2C ---
MPU_ADDR = 0x68
bus = smbus.SMBus(1)
try: bus.write_byte_data(MPU_ADDR, 0x6B, 0)
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

try: sensor_bme = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
except: 
    try: sensor_bme = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
    except: sensor_bme = None

if sensor_bme:
    sensor_bme.set_gas_status(bme680.ENABLE_GAS_MEAS)
    sensor_bme.set_gas_heater_temperature(320)
    sensor_bme.set_gas_heater_duration(150)
    sensor_bme.select_gas_heater_profile(0)

try: oled = sh1106(i2c(port=1, address=0x3C))
except: pass
try: font = ImageFont.truetype("DejaVuSans.ttf", 10)
except: font = ImageFont.load_default()

# --- FUNÇÃO DE UPLOAD ---
def upload_data(buffer):
    timestamp = int(time.time() * 1000)
    filename = f"sample_{timestamp}.json"
    print(f"\n[UPLOAD] Enviando {len(buffer)} amostras...", end="")
    
    payload = {
        "protected": { "ver": "v1", "alg": "HS256", "iat": time.time() },
        "signature": "EMPTY",
        "payload": {
            "device_name": DEVICE_NAME, "device_type": "RPI0",
            "interval_ms": (1000 / FREQUENCY_HZ),
            "sensors": [
                { "name": "temperature", "units": "Cel" },
                { "name": "gas", "units": "Ohm" },
                { "name": "vibration", "units": "g" },
                { "name": "audio", "units": "dB" }
            ],
            "values": buffer
        }
    }
    
    headers = {
        "x-api-key": EI_API_KEY,
        "x-file-name": filename,
        "x-label": LABEL_PADRAO,
        "Content-Type": "application/json"
    }
    
    try:
        res = requests.post(INGESTION_URL, json=payload, headers=headers)
        if res.status_code == 200:
            print(" SUCESSO!")
        else:
            print(f" FALHA ({res.status_code}): {res.text}")
    except Exception as e:
        print(f" ERRO: {e}")

# --- MAIN ---
if EI_API_KEY.startswith("ei_seu_numero"):
    print("ERRO: Configure sua API KEY na linha 20.")
    exit()

audio_t = threading.Thread(target=audio_thread_func)
audio_t.daemon = True 
audio_t.start()

print(f"\n--- COLETA VIA SDK V4 ({FREQUENCY_HZ}Hz) ---")
print(f"Label: {LABEL_PADRAO}")

interval = 1.0 / FREQUENCY_HZ
data_buffer = []

try:
    while True:
        loop_start = time.time()
        
        vib = read_mpu_raw()
        temp, gas = 0, 0
        if sensor_bme and sensor_bme.get_sensor_data():
            temp = sensor_bme.data.temperature
            if sensor_bme.data.heat_stable:
                gas = sensor_bme.data.gas_resistance
        
        data_buffer.append([temp, gas, vib, current_audio_db])
        
        if len(data_buffer) % 10 == 0:
            with canvas(oled) as draw:
                pct = len(data_buffer) / (FREQUENCY_HZ * SAMPLE_TIME_SEC) * 128
                draw.text((0, 0), f"GRAVANDO...", font=font, fill="white")
                draw.rectangle((0, 12, pct, 20), outline="white", fill="white")
                draw.text((0, 25), f"Amostras: {len(data_buffer)}", font=font, fill="white")
                draw.text((0, 38), f"Audio: {current_audio_db:.0f} dB", font=font, fill="white")
                draw.text((0, 50), f"Vib: {vib:.2f} g", font=font, fill="white")
        
        if len(data_buffer) >= (FREQUENCY_HZ * SAMPLE_TIME_SEC):
            upload_data(data_buffer)
            data_buffer = [] 
            print("Aguardando 2s...")
            time.sleep(2)
        
        elapsed = time.time() - loop_start
        if interval > elapsed:
            time.sleep(interval - elapsed)

except KeyboardInterrupt:
    print("\nParando...")