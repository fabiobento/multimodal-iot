import bme680
import time

# Inicializa o sensor
try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# Configurações de Oversampling (melhora precisão)
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

# --- Configuração do Sensor de GÁS ---
# Habilita o aquecedor para leitura de VOCs
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320) # 320 graus Celsius
sensor.set_gas_heater_duration(150)    # 150 milissegundos
sensor.select_gas_heater_profile(0)

print("Coletando dados do BME680... (Aguarde aquecimento)")

try:
    while True:
        if sensor.get_sensor_data():
            temp = sensor.data.temperature
            press = sensor.data.pressure
            hum = sensor.data.humidity
            
            # Formatação da saída
            output = "{0:.2f} C, {1:.2f} hPa, {2:.2f} %RH".format(temp, press, hum)
            
            # Leitura do Gás (Resistência em Ohms)
            # Quanto MAIOR a resistência, MAIS LIMPO é o ar.
            # Se a resistência cair drasticamente, detectou VOCs.
            if sensor.data.heat_stable:
                gas = sensor.data.gas_resistance
                output += ", Gás: {0:.2f} Ohms".format(gas)
            else:
                output += ", Aquecendo..."

            print(output)
            
        time.sleep(1)

except KeyboardInterrupt:
    pass