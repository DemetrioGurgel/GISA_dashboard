import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Adiciona o cliente ao grupo para receber atualizações
        await self.channel_layer.group_add("dashboard_group", self.channel_name)
        await self.accept()
        print("WebSocket conectado.")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("dashboard_group", self.channel_name)
        print("WebSocket desconectado.")

    # Este método será chamado quando o grupo enviar uma mensagem
    async def send_measurement(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))
