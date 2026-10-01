# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Llavero


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