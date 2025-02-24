from django.urls import path
from .views import dashboard, profile, historico

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('accounts/profile/', profile, name='profile'),
    path('historico/<str:parameter>/', historico, name='historico'),
]
