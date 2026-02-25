import pyaudio
import audioop
import math

# Configurações para o driver Google VoiceHAT
# Ele obriga a capturar em Estéreo (2 canais), mesmo o mic sendo Mono
CHANNELS = 2 
RATE = 48000
CHUNK = 4096 # Buffer maior para evitar engasgos
FORMAT = pyaudio.paInt32 # Formato de 32 bits

p = pyaudio.PyAudio()

# Procura o dispositivo correto automaticamente
device_index = None
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if "google" in info.get('name').lower():
        device_index = i
        print(f"Microfone encontrado: {info.get('name')} (Index {i})")
        break

if device_index is None:
    # Fallback: tenta o dispositivo padrão se não achar pelo nome
    device_index = 0
    print("Aviso: Driver 'google' não achado pelo nome. Usando índice 0.")

try:
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=CHUNK)
except Exception as e:
    print(f"\nERRO CRÍTICO: {e}")
    print("Dica: Verifique se nenhum outro programa está usando o microfone.")
    exit()

print("\n--- TESTE DE SOM ---")
print("Faça barulho perto do microfone (palmas, estalos)...")
print("[CTRL+C para sair]\n")

try:
    while True:
        # Lê os dados do microfone
        data = stream.read(CHUNK, exception_on_overflow=False)
        
        # O truque: Calculamos a energia (RMS) do som
        rms = audioop.rms(data, 4) 
        
        # Converte para uma escala visual
        if rms > 0:
            # Fórmula simples de decibéis para visualização
            db = 20 * math.log10(rms)
            
            # Limpa o ruído de fundo (ajuste esse 80 se precisar)
            meter = max(0, int(db - 140)) 
            
            bar = "█" * meter
            print(f"\rNível: {int(db)} |{bar:<40}|", end="")
        
except KeyboardInterrupt:
    print("\nTeste finalizado.")
    stream.stop_stream()
    stream.close()
    p.terminate()