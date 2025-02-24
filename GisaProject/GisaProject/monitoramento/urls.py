from django.urls import path
from .views import dashboard, profile

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('accounts/profile/', profile, name='profile'),
]
