from django.db import models
from django.db.models import ImageField, ForeignKey, CASCADE, BooleanField
from django.db.models.fields import (CharField, EmailField,
                                     PositiveIntegerField,
                                     DateTimeField)
from django.contrib.auth.models import User


# Create your models here.
class Direccion(models.Model):
    usuario = ForeignKey(User, on_delete=CASCADE,
                         related_name="direcciones")
    localidad = CharField(max_length=50)
    calle = CharField(max_length=100)
    numero = PositiveIntegerField()


class Mascota(models.Model):
    usuario = ForeignKey(User, on_delete=CASCADE, related_name="mascotas")
    nombre = CharField(max_length=50)
    imagen = ImageField(max_length=254, blank=True)
    sePerdio = BooleanField(default=False)


class Llavero(models.Model):
    mascota = ForeignKey(Mascota, on_delete=CASCADE, related_name="llaveros")
    codigo_activacion = CharField(max_length=254, unique=True)
    estado = CharField(max_length=100)
    identificador_publico = CharField(max_length=254, unique=True)


class Escaneo(models.Model):
    llavero = ForeignKey(Llavero, on_delete=CASCADE, related_name="llaveros")
    fecha = DateTimeField(auto_now_add=True)
    ubicacion = CharField(max_length=254)