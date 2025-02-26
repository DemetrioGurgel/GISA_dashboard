from django.urls import path
from .views import dashboard, profile, historico, latest_measurement, register_fiscal

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('accounts/profile/', profile, name='profile'),
    path('historico/<str:parameter>/', historico, name='historico'),
    path('api/latest/', latest_measurement, name='latest_measurement'),
    path('register-fiscal/', register_fiscal, name='register_fiscal'),
]

