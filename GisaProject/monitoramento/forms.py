from django import forms
from django.contrib.auth.models import User
from .models import FiscalProfile, SistemaAbastecimento

class FiscalRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    sistema = forms.ModelChoiceField(queryset=SistemaAbastecimento.objects.all())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        # Cria o usuário e define a senha
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Cria o FiscalProfile associado
            FiscalProfile.objects.create(user=user, sistema=self.cleaned_data['sistema'])
        return user
