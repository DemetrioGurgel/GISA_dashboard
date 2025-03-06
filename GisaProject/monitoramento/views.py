from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Measurement, FiscalProfile, SistemaAbastecimento
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .forms import FiscalRegistrationForm
from django.contrib.auth.decorators import user_passes_test


@login_required
def dashboard(request):
    # Se o usuário for superusuário, ele pode selecionar qual sistema visualizar.
    if request.user.is_superuser:
        sistemas = SistemaAbastecimento.objects.all()
        sistema_id = request.GET.get('sistema')
        if sistema_id:
            try:
                selected_sistema = SistemaAbastecimento.objects.get(id=sistema_id)
                measurements = Measurement.objects.filter(sistema=selected_sistema).order_by('-timestamp')
            except SistemaAbastecimento.DoesNotExist:
                selected_sistema = None
                measurements = Measurement.objects.none()
        else:
            selected_sistema = None
            measurements = Measurement.objects.none()  # ou measurements = Measurement.objects.all() se preferir exibir todos

        # Se não houver medições, cria uma instância temporária com valores zerados
        if not measurements.exists():
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
        else:
            measurement = measurements.first()

        context = {
            'sistemas': sistemas,
            'selected_sistema': selected_sistema,
            'measurement': measurement,
        }
    else:
        # Para usuários fiscais, filtra as medições pelo sistema associado ao perfil
        try:
            fiscal_profile = request.user.fiscal_profile
            sistema = fiscal_profile.sistema
            measurements = Measurement.objects.filter(sistema=sistema).order_by('-timestamp')
        except FiscalProfile.DoesNotExist:
            measurements = Measurement.objects.none()

        if not measurements.exists():
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
        else:
            measurement = measurements.first()

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

@login_required
@require_GET
def latest_measurement(request):
    measurement = Measurement.objects.order_by('-timestamp').first()
    if measurement is None:
        data = {}
    else:
        data = {
            'temperatura': measurement.temperatura,
            'ph': measurement.ph,
            'orp': measurement.orp,
            'turbidez': measurement.turbidez,
            'condutividade': measurement.condutividade,
            'nivel': measurement.nivel,
            'pressao': measurement.pressao,
            'frequencia': measurement.frequencia,
        }
    return JsonResponse(data)

def superuser_required(view_func):
    """Decorator para permitir acesso somente a superusuários."""
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@superuser_required
def register_fiscal(request):
    if request.method == 'POST':
        form = FiscalRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # ou para outra página de confirmação
    else:
        form = FiscalRegistrationForm()
    return render(request, 'register_fiscal.html', {'form': form})