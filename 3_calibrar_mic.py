import pyaudio
import audioop
import math
import time
from ctypes import *
from contextlib import contextmanager

# --- SILENCIADOR ALSA ---
# Esconde os avisos "Unknown PCM" que poluem a tela
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
    except: yield

# --- CONFIGURAÇÃO ---
CHUNK = 2048
FORMAT = pyaudio.paInt32
CHANNELS = 1 # O microfone I2S está ligado em Mono
RATE = 48000

with no_alsa_error():
    p = pyaudio.PyAudio()

# --- ACHA O MICROFONE CORRETO ---
dev_index = -1
for i in range(p.get_device_count()):
    try:
        info = p.get_device_info_by_index(i)
        # Exige que tenha o nome "google" E que seja capaz de gravar
        if "google" in info.get('name').lower() and info.get('maxInputChannels') > 0:
            dev_index = i
            break
    except: pass

if dev_index == -1:
    print("ERRO: Microfone de gravação não encontrado!")
    p.terminate()
    exit()

try:
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                    input=True, input_device_index=dev_index, 
                    frames_per_buffer=CHUNK)
except Exception as e:
    print(f"Erro ao abrir o stream: {e}")
    p.terminate()
    exit()

print("\n--- MODO DE CALIBRAÇÃO ---")
print("Fique em silêncio e observe o valor 'Base'.")
print("Faça barulho para ver o 'Pico'.")
print("Ctrl+C para sair.\n")

try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        rms = audioop.rms(data, 4)
        
        if rms > 0:
            db = 20 * math.log10(rms)
            # O flush=True força o terminal a atualizar a linha na mesma hora
            print(f"\rNível Atual (dB Matemático): {int(db)} dB      ", end="", flush=True)
        else:
            print("\rNível Atual (dB Matemático): 0 dB (Silêncio)  ", end="", flush=True)
        
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n\nSaindo da calibração...")
    stream.stop_stream()
    stream.close()
    p.terminate()