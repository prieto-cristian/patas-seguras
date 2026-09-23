from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.views import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import UsuarioRegistroForm, MascotaForm
from .models import Usuario, Mascota

# Create your views here.

def inicio(request):
    return render(request, 'index.html')


class UsuarioListView(ListView):
    model = Usuario
    context_object_name = "usuarios"
    template_name = "usuario_listado.html"


class UsuarioCreateView(CreateView):
    model = Usuario
    form_class = UsuarioRegistroForm
    template_name = 'usuario_formulario.html'
    success_url = reverse_lazy('listar_usuarios')


class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = UsuarioRegistroForm
    template_name = 'usuario_modificacion.html'
    success_url = reverse_lazy('listar_usuarios')


class MascotaListView(ListView):
    model = Mascota
    template_name = "mascota_listado.html"
    context_object_name = "mascotas"


class MascotaCreateView(CreateView):
    model = Mascota
    form_class = MascotaForm
    template_name = "mascota_formulario.html"
    success_url = reverse_lazy("listar_mascotas")


class MascotaUpdateView(UpdateView):
    model = Mascota
    form_class = MascotaForm
    template_name = "mascota_modificacion.html"
    success_url = reverse_lazy("listar_mascotas")


class RegistraseView(FormView):
    form_class = UsuarioRegistroForm
    template_name = "registrarse.html"
    success_url = reverse_lazy("listar_mascotas")

    def form_valid(self, form: UsuarioRegistroForm):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class IniciarSesionView(FormView):
    template_name = "iniciar_sesion.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("listar_mascotas")

    def form_valid(self, form : AuthenticationForm):
        login(self.request, form.get_user())
        return super().form_valid(form)


def cerrar_sesion(request):
    logout(request)
    return redirect("inicio")