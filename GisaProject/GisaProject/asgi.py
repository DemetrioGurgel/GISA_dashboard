import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from monitoramento.consumers import DashboardConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GisaProject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path("ws/dashboard/", DashboardConsumer.as_asgi()),
    ]),
})
