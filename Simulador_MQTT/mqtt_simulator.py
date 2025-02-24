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

# Cria e configura o cliente MQTT usando a nova API de callbacks
mqtt_client = mqtt.Client(client_id=client_id)
mqtt_client.on_connect = on_connect
mqtt_client.connect(broker_address, port, 60)

# Define um MAC Address fixo para simular um único dispositivo
mac_address = "00B0D063C226"

while True:
    # Cria os dados da mensagem com os parâmetros do monitoramento de água
    message_data = {
        "MACAddress": mac_address,
        "temperatura": round(random.uniform(0, 100), 2),   # valor entre 0 e 100 °C
        "ph": round(random.uniform(0, 14), 2),              # valor entre 0 e 14
        "orp": round(random.uniform(0, 500), 2),            # em mV
        "turbidez": round(random.uniform(0, 5), 2),         # em NTU
        "condutividade": round(random.uniform(0, 2000), 2), # em µS/cm
        "nivel": round(random.uniform(0, 100), 2),          # em cm
        "pressao": round(random.uniform(0, 10), 2),         # em kPa, por exemplo
        "frequencia": round(random.uniform(0, 100), 2)      # em Hz
    }

    message_payload = json.dumps(message_data)

    mqtt_client.publish(topic, message_payload)
    print(f"Mensagem enviada: {message_data}")

    time.sleep(2)
