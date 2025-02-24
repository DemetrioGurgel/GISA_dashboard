from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Measurement
from django.utils import timezone
from datetime import timedelta
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

@login_required
def historico(request, parameter):
    # Obter os parâmetros de filtro (opcional)
    # Por exemplo, start_date e end_date via GET
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Por padrão, exibir dados dos últimos 30 dias, se não for informado filtro
    if not start_date or not end_date:
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
    else:
        # Aqui você pode converter as strings para objetos datetime
        from datetime import datetime
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Filtra as medições no intervalo
    measurements = Measurement.objects.filter(timestamp__range=[start_date, end_date]).order_by('timestamp')

    # Prepare os dados para o gráfico: listas de timestamps e valores do parâmetro
    timestamps = [m.timestamp.strftime('%Y-%m-%d %H:%M') for m in measurements]
    # Certifique-se de que o nome do campo existe no modelo
    values = [getattr(m, parameter, None) for m in measurements]

    context = {
        'parameter': parameter.capitalize(),
        'timestamps': timestamps,
        'values': values,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    }
    return render(request, 'historico.html', context)