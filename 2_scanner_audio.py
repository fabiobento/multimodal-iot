import pyaudio

p = pyaudio.PyAudio()

print("\n--- RELATÓRIO DE DISPOSITIVOS DE ÁUDIO ---")
print(f"Total de dispositivos: {p.get_device_count()}\n")

for i in range(p.get_device_count()):
    try:
        info = p.get_device_info_by_index(i)
        name = info.get('name')
        inputs = info.get('maxInputChannels')
        rate = info.get('defaultSampleRate')
        
        # Filtra apenas o que interessa
        if "google" in name.lower() or inputs > 0:
            print(f"Index {i}: {name}")
            print(f"   > Canais de Entrada Máximos: {inputs}")
            print(f"   > Taxa de Amostragem Padrão: {rate}")
            print("-" * 30)
    except:
        pass

p.terminate()