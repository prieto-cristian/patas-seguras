from django.db import models
from django.db.models import (ImageField, ForeignKey, CASCADE, BooleanField,
                              OneToOneField, CharField, DateTimeField)
import hashlib
import secrets
from django.contrib.auth.models import User


# Create your models here.
class Perfil(models.Model):
    usuario = OneToOneField(User, on_delete=CASCADE, related_name="perfil")
    telefono = CharField(max_length=254, blank=True)
    facebook = CharField(max_length=254, blank=True)
    instagram = CharField(max_length=254, blank=True)
    whatsapp = CharField(max_length=254, blank=True)



class Direccion(models.Model):
    perfil = OneToOneField(Perfil, on_delete=CASCADE, related_name="direccion")
    localidad = CharField(max_length=50)
    calle = CharField(max_length=100)
    numero = CharField(max_length=14)


class Mascota(models.Model):
    nombre = CharField(max_length=50)
    imagen = ImageField(max_length=254, blank=True)
    sePerdio = BooleanField(default=False)


class Llavero(models.Model):
    ''' relacion con mascota es PROTECT porque no quiero eliminar el llavero
    cuando se desvincula una mascota. '''

    ESTADOS = [("NUEVO", "Nuevo"),("VINCULADO", "Vinculado"),
               ("EXPIRO", "Expiró"),]

    mascota = models.OneToOneField(Mascota,
        on_delete=models.PROTECT,
        related_name="llavero",
        null=True,
        blank=True
    )
    codigo_activacion = models.CharField(
        max_length=254,
        unique=True,
        blank=True  # Se genera automáticamente
    )
    estado = models.CharField(
        max_length=100,
        default="NUEVO",
        choices=ESTADOS
    )
    identificador_publico = models.CharField(
        max_length=254,
        unique=True,
        blank=True  # Se genera automáticamente
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE, related_name="llaveros")

    class Meta:
        verbose_name = "Llavero"
        verbose_name_plural = "Llaveros"

    def __str__(self):
        return f"{self.identificador_publico} - {self.estado}"

    def generar_identificador_publico(self):
        """
        Genera un identificador público único basado en el pk usando SHA256
        """
        if self.pk:
            hash_object = hashlib.sha256(
                f"{self.pk}-{self.__class__.__name__}".encode()
            )
            return hash_object.hexdigest()[:32]  # Primeros 32 caracteres
        return None

    def generar_codigo_activacion(self):
        """
        Genera un código de activación más corto usando secrets
        """
        # Combinamos pk + random para mayor seguridad
        if self.pk:
            data = f"{self.pk}-{secrets.token_hex(8)}"
            hash_object = hashlib.sha256(data.encode())
            return hash_object.hexdigest()[:10]  # Primeros 10 caracteres
        return None

    def save(self, *args, **kwargs):
        # Primera vez que se guarda (creación)
        if not self.pk:
            # Guardar primero para obtener el pk
            super().save(*args, **kwargs)

        # Generar los campos automáticos si están vacíos
        if not self.identificador_publico:
            self.identificador_publico = self.generar_identificador_publico()

        if not self.codigo_activacion:
            self.codigo_activacion = self.generar_codigo_activacion()

        # Guardar nuevamente con los valores generados
        super().save(*args, **kwargs)


class Escaneo(models.Model):
    llavero = ForeignKey(Llavero, on_delete=CASCADE, related_name="llaveros")
    fecha = DateTimeField(auto_now_add=True)
    ubicacion = CharField(max_length=254)