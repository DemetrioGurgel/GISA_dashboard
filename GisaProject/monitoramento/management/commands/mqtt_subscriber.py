import os
import json
import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Inicia o subscriber MQTT para receber dados dos sensores.'

    def handle(self, *args, **kwargs):
        # Certifique-se de que as configurações do Django já foram carregadas.
        # (O comando já roda com o settings configurado pelo manage.py)

        # Importa o modelo dentro do comando (após configurar o Django)
        from monitoramento.models import Measurement

        broker_address = "mqtt.eclipseprojects.io"
        port = 1883
        topic = "monitoramento_agua/servidor"

        client_id = f'django-mqtt-{os.getpid()}'
        mqtt_client = mqtt.Client(client_id=client_id)

        def on_connect(client, userdata, flags, rc, properties=None):
            if rc == 0:
                self.stdout.write(self.style.SUCCESS("Conexão MQTT estabelecida!"))
                # Inscreve-se no tópico para receber todas as mensagens publicadas nele
                client.subscribe(topic)
            else:
                self.stdout.write(self.style.ERROR(f"Erro na conexão, código {rc}"))

        def on_message(client, userdata, msg):
            self.stdout.write(f"Mensagem recebida no tópico {msg.topic}")
            try:
                payload = json.loads(msg.payload.decode('utf-8'))
                # Exemplo: o payload contém as chaves definidas no simulador
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
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao processar a mensagem: {e}"))

        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message

        self.stdout.write("Conectando ao broker MQTT...")
        mqtt_client.connect(broker_address, port, 60)

        # Inicia o loop para aguardar e processar mensagens
        mqtt_client.loop_forever()
