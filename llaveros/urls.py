from django.urls import path
from .views import (inicio, MascotaListView,
                    MascotaCreateView, MascotaUpdateView, LlaveroView,
                    LlaveroVincularView, MensajeLlaveroExitosoView, MascotaDetailView,
                    LlaveroListView, LlaveroUpdateView)

urlpatterns = [
    path("", inicio, name='inicio'),
    path("mascotas/", MascotaListView.as_view(), name="listar_mascotas"),
    path("mascotas/crear/", MascotaCreateView.as_view(), name="crear_mascota"),
    path("mascotas/modificar/<pk>/", MascotaUpdateView.as_view(), name="modificar_mascota"),
    path("llavero/<slug:slug>/", LlaveroView.as_view(), name="mostrar_llavero"),
    path("llavero/vincular/<slug:slug>/", LlaveroVincularView.as_view(), name="registrar_llavero"),
    path("llavero/vincular/exito", MensajeLlaveroExitosoView.as_view(), name="registro_llavero_exitoso"),
    path("mascotas/mascota/<slug:slug>/", MascotaDetailView.as_view(), name="informacion_mascota"),
    path("llaveros/", LlaveroListView.as_view(), name="listar_llaveros"),
    path("llaveros/llavero/modificar/<slug:slug>", LlaveroUpdateView.as_view(), name="modificar_llavero"),
]