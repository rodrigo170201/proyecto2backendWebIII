from django.db import models


class Movimiento(models.Model):
    TIPO_MOVIMIENTO = [
        ('INGRESO', 'INGRESO'),
        ('EGRESO', 'EGRESO'),
        ('TRANSFERENCIA_ENVIADA', 'TRANSFERENCIA_ENVIADA'),
        ('TRANSFERENCIA_RECIBIDA', 'TRANSFERENCIA_RECIBIDA'),
    ]
    cuenta = models.ForeignKey('Cuenta', on_delete=models.CASCADE, related_name='movimientos')
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=25, choices=TIPO_MOVIMIENTO)
    monto = models.DecimalField(decimal_places=2, max_digits=12)
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.get_tipo_display()} {self.monto} en {self.cuenta.numero_cuenta} - {self.fecha:%Y-%m-%d %H:%M}"