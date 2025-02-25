from django.urls import path
from .views import dashboard, profile, historico, latest_measurement

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('accounts/profile/', profile, name='profile'),
    path('historico/<str:parameter>/', historico, name='historico'),
    path('api/latest/', latest_measurement, name='latest_measurement'),
]

