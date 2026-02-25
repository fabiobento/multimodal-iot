import time
import subprocess
from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106, ssd1306 # Importamos ambos para testar

# --- Configuração do Hardware ---
# Cria a interface I2C
serial = i2c(port=1, address=0x3C)

# TENTATIVA 1: Inicializa como SH1106 (O provável culpado)
# Se a tela continuar ruim, troque "sh1106" por "ssd1306" na linha abaixo
device = sh1106(serial) 
# device = ssd1306(serial) # Descomente esta e comente a de cima se não funcionar

print("Display inicializado. Pressione Ctrl+C para sair.")

# Carrega a fonte (mesma lógica do seu código anterior)
try:
    font = ImageFont.truetype("DejaVuSans.ttf", 10)
except IOError:
    font = ImageFont.load_default()

try:
    while True:
        # A biblioteca Luma usa o objeto 'canvas' que limpa a tela e desenha automaticamente
        with canvas(device) as draw:
            # --- Coleta de Dados ---
            cmd = "hostname -I | cut -d' ' -f1"
            IP = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            
            cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
            CPU = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()

            # --- Desenho ---
            # Desenha um retângulo de fundo (opcional, o canvas já limpa, mas garante borda)
            # draw.rectangle(device.bounding_box, outline="white", fill="black")
            
            draw.text((0, 0), "PROJETO BRICKML", font=font, fill="white")
            draw.line((0, 12, 128, 12), fill="white")
            draw.text((0, 15), f"IP: {IP}", font=font, fill="white")
            draw.text((0, 25), f"{CPU}", font=font, fill="white")
            draw.text((0, 35), "Status: Monitorando...", font=font, fill="white")

        # Não precisa de oled.show() ou time.sleep() longo, 
        # mas damos uma pausa para não consumir 100% da CPU atualizando a tela
        time.sleep(1)

except KeyboardInterrupt:
    # Limpa a tela ao sair
    device.cleanup()
    print("Encerrado.")