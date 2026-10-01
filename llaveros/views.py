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
from .forms import (UsuarioRegistroForm, MascotaForm, UsuarioUpdateForm,
                    LlaveroForm, LlaveroFormActivacion, DireccionForm,
                    RedesSocialesForm)
from .models import Mascota, Llavero, Perfil, Direccion

# Create your views here.

def inicio(request):
    return render(request, 'index.html')


class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UsuarioUpdateForm
    template_name = 'configuracion_perfil.html'
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


class MascotaCreateView(CreateView):
    model = Mascota
    form_class = MascotaForm
    template_name = "mascota_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.llavero = get_object_or_404(
            Llavero,
            identificador_publico=kwargs["slug"],
            usuario=request.user
        )

        if self.llavero.mascota is not None:
            return redirect(
                "configurar_llavero",
                slug=self.llavero.identificador_publico
            )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        mascota = form.save()

        self.llavero.mascota = mascota
        self.llavero.estado = "VINCULADO"
        self.llavero.save()

        return redirect(
            "configurar_llavero",
            slug=self.llavero.identificador_publico
        )


class RegistrarseView(FormView):
    form_class = UsuarioRegistroForm
    template_name = "registrarse.html"
    success_url = reverse_lazy("inicio")

    def form_valid(self, form: UsuarioRegistroForm):
        user = form.save()
        user.email = form.cleaned_data['email']
        user.save()
        perfil= Perfil.objects.create(usuario=user)
        Direccion.objects.create(perfil=perfil)
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
        llavero = get_object_or_404(Llavero,
                                    identificador_publico=kwargs["slug"])

        match llavero.estado:
            case "NUEVO":
                if request.user.is_authenticated:
                    return redirect("registrar_llavero",
                                    slug=llavero.identificador_publico)
                return render(request, "mensaje_registrese_inicie_sesion.html")

            case "VINCULADO":
                if llavero.mascota:
                    return render(request, "llavero_publico.html", {
                        'llavero': llavero,
                    })

            case "EXPIRO":
                return redirect("llavero_expiro")

        return HttpResponseNotFound("No se encontro")

class LlaveroVincularView(View):

    def get(self, request, **kwargs):
        llavero = get_object_or_404(Llavero,identificador_publico=kwargs['slug'],
                                    estado="NUEVO", usuario=None)

        form = LlaveroFormActivacion()

        return render(request,"vincular_llavero.html",{
                "form": form,
                "llavero": llavero,
                "slug" : llavero.identificador_publico,
        })

    def post(self, request, **kwargs):
        llavero = get_object_or_404(Llavero,identificador_publico=kwargs['slug'],
                                    estado="NUEVO")

        form = LlaveroFormActivacion(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data["codigo_activacion"]
            if llavero.codigo_activacion == codigo:
                llavero.usuario = request.user
                llavero.estado = "VINCULADO"
                llavero.save()

                return render(request, "registro_llavero_exitoso.html")

        return render(request,"vincular_llavero.html",{
                "form": form,
                "llavero": llavero,
                "slug": llavero.identificador_publico,
                "error": "El código de activación no es válido.",
        })


class LlaveroListView(ListView):
    model = Llavero
    context_object_name = "llaveros"
    template_name = "listar_llaveros.html"

    def get_queryset(self):
        return Llavero.objects.filter(usuario=self.request.user)


class DireccionUpdateView(UpdateView):
    model = Direccion
    form_class = DireccionForm
    template_name = "configuracion_direccion.html"
    success_url = reverse_lazy("inicio")

    def get_queryset(self):
        return Direccion.objects.filter(pk=self.kwargs['pk'], perfil__usuario=self.request.user)


class RedesUpdateView(UpdateView):
    model = Perfil
    form_class = RedesSocialesForm
    template_name = "configuracion_redes_sociales.html"
    success_url = reverse_lazy("inicio")

    def get_queryset(self):
        return Perfil.objects.filter(pk=self.kwargs["pk"], usuario=self.request.user)


class LlaveroConfiguracionView(DetailView):
    model = Llavero
    slug_field = "identificador_publico"
    template_name = "llavero_configuracion.html"
    context_object_name = "llavero"

    def get_queryset(self):
        return Llavero.objects.filter(usuario=self.request.user)


class MascotaUpdateView(UpdateView):
    model = Mascota
    form_class = MascotaForm
    template_name = "mascota_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.llavero = get_object_or_404(
            Llavero,
            identificador_publico=kwargs["slug"],
            usuario=request.user
        )

        if self.llavero.mascota is None:
            return redirect(
                "configurar_llavero",
                slug=self.llavero.identificador_publico
            )

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.llavero.mascota

    def form_valid(self, form):
        form.save()

        return redirect(
            "configurar_llavero",
            slug=self.llavero.identificador_publico
        )