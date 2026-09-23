from django.urls import path
from .views import (inicio, UsuarioUpdateView, MascotaListView,
                    MascotaCreateView, MascotaUpdateView, LlaveroDetailView)

urlpatterns = [
    path("", inicio, name='inicio'),
    path('usuarios/modificar/<pk>/', UsuarioUpdateView.as_view(), name="modificar_usuario"),

    path("mascotas/", MascotaListView.as_view(), name="listar_mascotas"),
    path("mascotas/crear/", MascotaCreateView.as_view(), name="crear_mascota"),
    path("mascotas/modificar/<pk>/", MascotaUpdateView.as_view(), name="modificar_mascota"),
    path("llavero/<slug:slug>/", LlaveroDetailView.as_view(), name="mostrar_llavero"),
]