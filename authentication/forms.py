from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Assure-toi que CustomUser est bien défini dans models.py


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
    def clean_username(self):
        username = self.cleaned_data['username']
        if username.lower() == "localhost@localhost.localhost".lower():
            raise forms.ValidationError("Ce nom d'utilisateur n'est pas autorisé.")
        if "localhost" in username.lower():
            raise forms.ValidationError("Le mot 'localhost' n'est pas autorisé dans le nom d'utilisateur.")
        return username