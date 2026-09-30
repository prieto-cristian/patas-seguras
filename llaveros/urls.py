from django.urls import path
from .views import (inicio, UsuarioUpdateView, MascotaListView,
                    MascotaCreateView, MascotaUpdateView, LlaveroView,
                    LlaveroVincularView)

urlpatterns = [
    path("", inicio, name='inicio'),
    path('usuarios/modificar/<pk>/', UsuarioUpdateView.as_view(), name="modificar_usuario"),

    path("mascotas/", MascotaListView.as_view(), name="listar_mascotas"),
    path("mascotas/crear/", MascotaCreateView.as_view(), name="crear_mascota"),
    path("mascotas/modificar/<pk>/", MascotaUpdateView.as_view(), name="modificar_mascota"),
    path("llavero/<slug:slug>/", LlaveroView.as_view(), name="mostrar_llavero"),
    path("llavero/vincular/<slug:slug>/", LlaveroVincularView.as_view(), name="registrar_llavero"),
]