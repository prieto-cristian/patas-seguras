from django import forms
from .models import Usuario, Mascota

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ("nombre", "apellido", "email", "telefono")


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ("nombre", "estado", "imagen", "usuario")