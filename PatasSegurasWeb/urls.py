"""
URL configuration for PatasSegurasWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from llaveros.views import (RegistrarseView, IniciarSesionView, cerrar_sesion,
                            UsuarioUpdateView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("llaveros.urls")),
    path("registrarse/", RegistrarseView.as_view(), name="registrarse"),
    path("registrarse/perfil", RegistrarseView.as_view(), name="crear_perfil"),
    path("iniciar_sesion/", IniciarSesionView.as_view(), name="iniciar_sesion"),
    path("cerrar_sesion/", cerrar_sesion, name="cerrar_sesion"),
    path('usuarios/modificar/<pk>/', UsuarioUpdateView.as_view(), name="modificar_usuario"),
]
