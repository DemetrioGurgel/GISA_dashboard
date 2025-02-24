from django.db import models
from django.contrib.auth.models import User

class WaterSystem(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Device(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    water_system = models.ForeignKey(WaterSystem, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.device_id

class Measurement(models.Model):
    mac_address = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    temperatura = models.FloatField()
    ph = models.FloatField()
    orp = models.FloatField()
    turbidez = models.FloatField()
    condutividade = models.FloatField()
    nivel = models.FloatField()
    pressao = models.FloatField()
    frequencia = models.FloatField()

    def __str__(self):
        return f"Medicao {self.mac_address} em {self.timestamp}"

# Perfil para usuários fiscais, relacionando-os aos sistemas de água
class FiscalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    water_systems = models.ManyToManyField(WaterSystem)

    def __str__(self):
        return self.user.username
