from django.contrib import admin
from .models import WaterSystem, Device, Measurement, FiscalProfile, Estado, Municipio, SistemaAbastecimento

admin.site.register(WaterSystem)
admin.site.register(Device)
admin.site.register(Measurement)
#admin.site.register(FiscalProfile)

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla')

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estado')
    list_filter = ('estado',)

@admin.register(SistemaAbastecimento)
class SistemaAbastecimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'municipio')
    list_filter = ('municipio__estado', 'municipio')

@admin.register(FiscalProfile)
class FiscalProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'sistema')
    list_filter = ('sistema__municipio__estado', 'sistema')