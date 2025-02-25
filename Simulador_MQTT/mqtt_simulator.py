import json
import random
import time
import paho.mqtt.client as mqtt

# Configurações do Broker MQTT
broker_address = "mqtt.eclipseprojects.io"
port = 1883
topic = "monitoramento_agua/servidor"
client_id = f'python-mqtt-{random.randint(0, 10000)}'

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Conexão MQTT estabelecida!")
    else:
        print(f"Erro na conexão, código de erro {rc}")

mqtt_client = mqtt.Client(client_id=client_id)
mqtt_client.on_connect = on_connect
mqtt_client.connect(broker_address, port, 60)

# Define um MAC Address fixo para simular um único dispositivo
mac_address = "00B0D063C226"

# Valores iniciais para cada parâmetro (base)
base_temperatura = 25.0       # °C
base_ph = 7.0                 # pH neutro
base_orp = 150.0              # mV
base_turbidez = 1.0           # NTU
base_condutividade = 500.0    # µS/cm
base_nivel = 50.0             # cm
base_pressao = 5.0            # kPa
base_frequencia = 50.0        # Hz

while True:
    # Atualiza cada valor com uma pequena variação aleatória
    base_temperatura += random.uniform(-0.5, 0.5)
    base_ph += random.uniform(-0.1, 0.1)
    base_orp += random.uniform(-5, 5)
    base_turbidez += random.uniform(-0.1, 0.1)
    base_condutividade += random.uniform(-20, 20)
    base_nivel += random.uniform(-1, 1)
    base_pressao += random.uniform(-0.5, 0.5)
    base_frequencia += random.uniform(-2, 2)

    # Garante que os valores permaneçam em intervalos realísticos
    base_temperatura = max(0, min(100, base_temperatura))
    base_ph = max(0, min(14, base_ph))
    base_orp = max(0, min(500, base_orp))
    base_turbidez = max(0, min(5, base_turbidez))
    base_condutividade = max(0, min(2000, base_condutividade))
    base_nivel = max(0, min(100, base_nivel))
    base_pressao = max(0, min(10, base_pressao))
    base_frequencia = max(0, min(100, base_frequencia))

    message_data = {
        "MACAddress": mac_address,
        "temperatura": round(base_temperatura, 2),
        "ph": round(base_ph, 2),
        "orp": round(base_orp, 2),
        "turbidez": round(base_turbidez, 2),
        "condutividade": round(base_condutividade, 2),
        "nivel": round(base_nivel, 2),
        "pressao": round(base_pressao, 2),
        "frequencia": round(base_frequencia, 2)
    }

    message_payload = json.dumps(message_data)
    mqtt_client.publish(topic, message_payload)
    print(f"Mensagem enviada: {message_data}")

    time.sleep(2)
