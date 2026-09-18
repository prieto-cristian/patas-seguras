from django.urls import path
from .views import (inicio, UsuarioListView, UsuarioCreateView,
                    UsuarioUpdateView)

urlpatterns = [
    path("", inicio, name='inicio'),
    path("usuarios/", UsuarioListView.as_view(), name="listar_usuarios"),
    path("usuarios/crear/", UsuarioCreateView.as_view(), name="crear_usuario"),
    path('usuarios/modificar/<pk>/', UsuarioUpdateView.as_view(), name="modificar_usuario"),
]