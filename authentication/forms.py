from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Assure-toi que CustomUser est bien défini dans models.py


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
