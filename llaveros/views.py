from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, TemplateView
from django.views import View
from django.contrib.auth.views import FormView
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .forms import UsuarioRegistroForm, MascotaForm, UsuarioUpdateForm, LlaveroForm
from .models import Mascota, Llavero

# Create your views here.

def inicio(request):
    return render(request, 'index.html')


class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UsuarioUpdateForm
    template_name = 'usuario_modificacion.html'
    success_url = reverse_lazy('listar_mascotas')
    login_url = 'login'  # Redirige a login si no está autenticado

    def get_object(self, queryset=None):
        # Retorna el usuario actualmente logueado
        return self.request.user

    def form_valid(self, form):
        # Verificación adicional de seguridad
        if form.instance.pk != self.request.user.pk:
            raise PermissionDenied("No tienes permiso para editar este usuario")
        return super().form_valid(form)


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


class LlaveroView(View):

    def get(self, request, *args, **kwargs):
        llavero = get_object_or_404(
            Llavero,
            identificador_publico=kwargs["slug"] )

        match llavero.estado:
            case "NUEVO":
                if request.user.is_authenticated:
                    return redirect("registrar_llavero",
                                    slug=llavero.identificador_publico)
                return redirect("login")

            case "VINCULADO":
                return redirect("informacion_mascota",
                                slug=llavero.identificador_publico)

            case "EXPIRO":
                return redirect("llavero_expiro")

            case "SIN_MASCOTA":
                return redirect("llavero_sin_mascota")
        return Http404("No se encontro")


class LlaveroVincularView(TemplateView):
    template_name = 'vincular_llavero.html'

    def post(self, slug):
        llavero = get_object_or_404(Llavero, identificador_publico=slug)
        print(f"LLAVERO: {llavero}")
        pass
