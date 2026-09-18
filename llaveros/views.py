from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from .forms import UsuarioForm
from .models import Usuario

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
    template_name = 'usuario_creacion.html'
    success_url = reverse_lazy('listar_usuarios')


class UsuarioUpdateView(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario_modificacion.html'
    success_url = reverse_lazy('listar_usuarios')