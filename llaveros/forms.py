from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Mascota

class UsuarioRegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ("nombre", "imagen", "usuario")


class UsuarioUpdateForm(UserChangeForm):
    password = forms.CharField(
        label='Cambiar contraseña (dejar en blanco para no cambiar)',
        required=False,
        widget=forms.PasswordInput(),
        help_text="Dejar vacío si no deseas cambiar la contraseña"
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Elimina el campo de password predeterminado de UserChangeForm
        if 'password' in self.fields:
            del self.fields['password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            # Validaciones básicas de contraseña
            if len(password) < 8:
                raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)

        if commit:
            user.save()
        return user