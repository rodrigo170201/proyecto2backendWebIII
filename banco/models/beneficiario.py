from django.db import models
from rest_framework.exceptions import ValidationError

from banco.models.cuenta import Cuenta
from banco.models.usuario import Usuario


class Beneficiario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='beneficiarios')
    nombre = models.CharField(max_length=100)
    numero_cuenta = models.CharField(max_length=10)

    def valido(self):
        if not Cuenta.objects.filter(numero_cuenta=self.numero_cuenta).exists():
            raise ValidationError(f"La cuenta {self.numero_cuenta} no existe")

    def __str__(self):
        return f"{self.nombre} ({self.numero_cuenta})"