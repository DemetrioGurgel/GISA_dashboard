from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Measurement

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Measurement


@login_required
def dashboard(request):
    # Busca a medição mais recente
    measurement = Measurement.objects.order_by('-timestamp').first()

    # Se não houver medição, cria uma instância temporária com valores zerados
    if not measurement:
        measurement = Measurement(
            temperatura=0,
            ph=0,
            orp=0,
            condutividade=0,
            turbidez=0,
            nivel=0,
            pressao=0,
            frequencia=0
        )

    context = {
        'measurement': measurement,
    }
    return render(request, 'dashboard.html', context)


@login_required
def profile(request):
    return render(request, 'profile.html')