from django.db import models
from django.db.models import ImageField, ForeignKey, CASCADE
from django.db.models.fields import (CharField, EmailField,
                                     PositiveIntegerField, DateField,
                                     DateTimeField)


# Create your models here.
class Usuario(models.Model):
    nombre = CharField(max_length=50)
    apellido = CharField(max_length=50)
    email = EmailField(unique=True)
    telefono = CharField(max_length=50)


class Direccion(models.Model):
    usuario = ForeignKey(Usuario, on_delete=CASCADE,
                         related_name="direcciones")
    localidad = CharField(max_length=50)
    calle = CharField(max_length=100)
    numero = PositiveIntegerField()


class Mascota(models.Model):
    usuario = ForeignKey(Usuario, on_delete=CASCADE, related_name="mascotas")
    nombre = CharField(max_length=50)
    imagen = ImageField(max_length=254, blank=True)
    estado = CharField(max_length=50)


class Vacuna(models.Model):
    mascota = ForeignKey(Mascota, on_delete=CASCADE, related_name="vacunas")
    nombre = CharField(max_length=100)
    fecha_inyeccion = DateField()
    fecha_caduca = DateField()


class Llavero(models.Model):
    mascota = ForeignKey(Mascota, on_delete=CASCADE, related_name="llaveros")
    codigo_activacion = CharField(max_length=254, unique=True)
    estado = CharField(max_length=100)
    identificador_publico = CharField(max_length=254, unique=True)


class Escaneo(models.Model):
    llavero = ForeignKey(Llavero, on_delete=CASCADE, related_name="llaveros")
    fecha = DateTimeField(auto_now_add=True)
    ubicacion = CharField(max_length=254)