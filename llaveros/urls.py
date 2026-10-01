from django.urls import path
from .views import (inicio, MascotaCreateView, LlaveroView,
                    LlaveroVincularView, LlaveroListView,
                    LlaveroConfiguracionView, MascotaUpdateView)

urlpatterns = [
    path("", inicio, name='inicio'),

    path("llaveros/", LlaveroListView.as_view(), name="listar_llaveros"),

    path("llavero/<slug:slug>/", LlaveroView.as_view(),
         name="mostrar_llavero"),

    path("llavero/vincular/<slug:slug>/", LlaveroVincularView.as_view(),
         name="registrar_llavero"),

    path("llavero/<slug:slug>/configurar/",
         LlaveroConfiguracionView.as_view(), name="configurar_llavero"),

    path("llavero/<slug:slug>/configurar/mascota/crear/",
         MascotaCreateView.as_view(),name="crear_mascota_llavero"),

    path("llavero/<slug:slug>/configurar/mascota/",
         MascotaUpdateView.as_view(), name="modificar_mascota_llavero"),
]