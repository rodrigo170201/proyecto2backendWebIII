from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from banco.models import Cuenta, Movimiento


class MovimientoSerializer(serializers.ModelSerializer):
    numero_cuenta = serializers.CharField(source='cuenta.numero_cuenta', read_only=True)

    class Meta:
        model = Movimiento
        fields = ['id', 'cuenta', 'numero_cuenta', 'fecha', 'tipo', 'monto', 'descripcion']
        read_only_fields = ['fecha']

class MovimientoViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer

    def get_queryset(self):
        return Movimiento.objects.filter(cuenta__usuario=self.request.user).order_by('-fecha')