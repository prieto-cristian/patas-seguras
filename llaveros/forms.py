from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Usuario, Mascota

class UsuarioRegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ("nombre", "imagen", "usuario")