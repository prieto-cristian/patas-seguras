from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Mascota, Llavero, Direccion, Perfil

class UsuarioRegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email


class UsuarioUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")


class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ("localidad", "calle", "numero")


class RedesSocialesForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ("facebook", "instagram", "telefono", "whatsapp")


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ("nombre", "imagen", "usuario")


class LlaveroForm(forms.ModelForm):
    class Meta:
        model = Llavero
        fields = ("mascota",)


class LlaveroFormActivacion(forms.Form):
    codigo_activacion = forms.CharField(
        label="Código de activación",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Ingresá el código de activación"
        })
    )