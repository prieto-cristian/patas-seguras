# admin.py
from django.contrib import admin
from .models import Llavero, Perfil


@admin.register(Llavero)
class LlaverosAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "identificador_publico",
        "estado",
        "codigo_activacion",
        "mascota__usuario__username",
        "fecha_creacion"
    )
    list_filter = ("estado", "mascota__usuario")
    search_fields = ("identificador_publico", "codigo_activacion",
                     "mascota__usuario__username", "fecha_creacion")
    readonly_fields = (
        "pk",
        "identificador_publico",
        "codigo_activacion",
        "fecha_creacion",
        "mascota",
    )
    ordering = ["-fecha_creacion"]


admin.site.register(Perfil)