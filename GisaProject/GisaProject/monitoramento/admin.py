from django.contrib import admin
from .models import WaterSystem, Device, Measurement, FiscalProfile

admin.site.register(WaterSystem)
admin.site.register(Device)
admin.site.register(Measurement)
admin.site.register(FiscalProfile)
