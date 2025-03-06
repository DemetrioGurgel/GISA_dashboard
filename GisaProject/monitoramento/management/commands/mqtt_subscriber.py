import os
import json
import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class Command(BaseCommand):
    help = 'Inicia o subscriber MQTT para receber dados dos sensores.'

    def handle(self, *args, **kwargs):
        from monitoramento.models import Measurement

        broker_address = "mqtt.eclipseprojects.io"
        port = 1883
        topic = "monitoramento_agua/servidor"
        client_id = f'django-mqtt-{os.getpid()}'
        mqtt_client = mqtt.Client(client_id=client_id)

        channel_layer = get_channel_layer()

        def on_connect(client, userdata, flags, rc, properties=None):
            if rc == 0:
                self.stdout.write(self.style.SUCCESS("Conexão MQTT estabelecida!"))
                client.subscribe(topic)
            else:
                self.stdout.write(self.style.ERROR(f"Erro na conexão, código {rc}"))

        def on_message(client, userdata, msg):
            self.stdout.write(f"Mensagem recebida no tópico {msg.topic}")
            try:
                payload = json.loads(msg.payload.decode('utf-8'))
                Measurement.objects.create(
                    mac_address=payload.get("MACAddress"),
                    temperatura=payload.get("temperatura"),
                    ph=payload.get("ph"),
                    orp=payload.get("orp"),
                    turbidez=payload.get("turbidez"),
                    condutividade=payload.get("condutividade"),
                    nivel=payload.get("nivel"),
                    pressao=payload.get("pressao"),
                    frequencia=payload.get("frequencia")
                )
                self.stdout.write(self.style.SUCCESS("Medição salva com sucesso."))

                # Envia a medição para os clientes conectados via WebSocket
                async_to_sync(channel_layer.group_send)(
                    "dashboard_group",
                    {
                        "type": "send_measurement",  # Esse nome deve corresponder ao método do consumer
                        "data": payload,
                    }
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao processar a mensagem: {e}"))

        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message

        self.stdout.write("Conectando ao broker MQTT...")
        mqtt_client.connect(broker_address, port, 60)
        mqtt_client.loop_forever()
