from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from .forms import UsuarioForm, MascotaForm
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
    form_class = UsuarioForm
    template_name = 'usuario_formulario.html'
    success_url = reverse_lazy('listar_usuarios')


class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = UsuarioForm
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