from django.urls import path
from .views import (inicio, UsuarioListView, UsuarioCreateView,
                    UsuarioUpdateView, MascotaListView, MascotaCreateView,
                    MascotaUpdateView)

urlpatterns = [
    path("", inicio, name='inicio'),
    path("usuarios/", UsuarioListView.as_view(), name="listar_usuarios"),
    path("usuarios/crear/", UsuarioCreateView.as_view(), name="crear_usuario"),
    path('usuarios/modificar/<pk>/', UsuarioUpdateView.as_view(), name="modificar_usuario"),

    path("mascotas/", MascotaListView.as_view(), name="listar_mascotas"),
    path("mascotas/crear/", MascotaCreateView.as_view(), name="crear_mascota"),
    path("mascotas/modificar/<pk>/", MascotaUpdateView.as_view(), name="modificar_mascota"),
]