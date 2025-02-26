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

class Estado(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.nome} ({self.sigla})"


class Municipio(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name="municipios")

    def __str__(self):
        return f"{self.nome} - {self.estado.sigla}"


class SistemaAbastecimento(models.Model):
    nome = models.CharField(max_length=100)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, related_name="sistemas")
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.municipio})"


class Measurement(models.Model):
    sistema = models.ForeignKey(SistemaAbastecimento, on_delete=models.CASCADE, null=True, blank=True)
    mac_address = models.CharField(max_length=50)  # Campo para o MAC Address
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
        return f"Medicao {self.sistema} em {self.timestamp}"


class FiscalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="fiscal_profile")
    sistema = models.ForeignKey(SistemaAbastecimento, on_delete=models.CASCADE, related_name="fiscais")

    def __str__(self):
        return f"{self.user.username} - {self.sistema}"
