import random

from django.db import models

from banco.models.usuario import Usuario


def generar_numero_cuenta():
    return  ''.join(str(random.randint(0, 9)) for _ in range(10))

class Cuenta(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='cuentas')
    numero_cuenta = models.CharField(max_length=10, unique=True,default=generar_numero_cuenta)
    saldo = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)

    def __str__(self):
        return f"Cuenta {self.numero_cuenta} - {self.usuario.username}"
