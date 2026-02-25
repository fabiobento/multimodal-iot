import math
import smbus
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

# --- CONFIGURAÇÃO DE HARDWARE ---

# 1. Configuração do MPU6050
MPU_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
bus = smbus.SMBus(1)
try:
    bus.write_byte_data(MPU_ADDR, PWR_MGMT_1, 0)
except Exception as e:
    print(f"Erro MPU: {e}")

# 2. Configuração do OLED (SH1106)
try:
    serial = i2c(port=1, address=0x3C)
    device = sh1106(serial) 
except:
    print("Erro no Display")
    exit()

# --- ENGINE 3D SIMPLES ---

vertices = [
    [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
    [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
]

edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

def read_accel():
    try:
        raw_x = bus.read_byte_data(MPU_ADDR, ACCEL_XOUT_H)
        high_x, low_x = raw_x, bus.read_byte_data(MPU_ADDR, ACCEL_XOUT_H+1)
        
        raw_y = bus.read_byte_data(MPU_ADDR, ACCEL_XOUT_H+2)
        high_y, low_y = raw_y, bus.read_byte_data(MPU_ADDR, ACCEL_XOUT_H+3)
        
        # Simplifiquei a leitura do Z pois não usamos para rotação neste exemplo
        
        x = (high_x << 8) | low_x
        y = (high_y << 8) | low_y

        if x > 32768: x -= 65536
        if y > 32768: y -= 65536
        
        return x / 16384.0, y / 16384.0
    except:
        return 0, 0

def rotate(x, y, z, angle_x, angle_y):
    # Rotação X
    new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
    new_z = y * math.sin(angle_x) + z * math.cos(angle_x)
    y, z = new_y, new_z

    # Rotação Y
    new_x = x * math.cos(angle_y) - z * math.sin(angle_y)
    new_z = x * math.sin(angle_y) + z * math.cos(angle_y)
    x, z = new_x, new_z
    
    return x, y, z

# --- LOOP PRINCIPAL ---
print("Cubo 3D Reduzido. Mexa o sensor!")

last_ax, last_ay = 0, 0
ALPHA = 0.2

try:
    while True:
        ax, ay = read_accel()
        
        # Filtro
        ax = last_ax + ALPHA * (ax - last_ax)
        ay = last_ay + ALPHA * (ay - last_ay)
        last_ax, last_ay = ax, ay

        rot_x = ay * 3 
        rot_y = -ax * 3 

        with canvas(device) as draw:
            projected_points = []
            
            center_x = 64
            center_y = 32
            
            # --- AJUSTE FEITO AQUI ---
            # Reduzido de 20 para 10 para caber na tela
            scale = 10 

            for v in vertices:
                x, y, z = v[0], v[1], v[2]
                x, y, z = rotate(x, y, z, rot_x, rot_y)
                
                z_offset = 4
                
                # Projeção simplificada
                px = x * scale * 1.5 
                py = y * scale * 1.5
                
                projected_points.append([center_x + px, center_y + py])

            for edge in edges:
                p1 = projected_points[edge[0]]
                p2 = projected_points[edge[1]]
                draw.line((p1[0], p1[1], p2[0], p2[1]), fill="white")

except KeyboardInterrupt:
    pass