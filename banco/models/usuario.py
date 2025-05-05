# banco/models/usuario.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    nombre_completo = models.CharField(max_length=100)
    ci = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nombre_completo} ({self.username})"
