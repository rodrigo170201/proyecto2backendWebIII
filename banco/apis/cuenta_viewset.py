from decimal import Decimal, InvalidOperation

from django.http import Http404
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from banco.models import Usuario, Cuenta, Movimiento


class CuentaSerializer(serializers.ModelSerializer):
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault())
    numero_cuenta = serializers.CharField(read_only=True)
    saldo = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.nombre_completo',read_only=True)
    class Meta:
        model = Cuenta
        fields = ['id', 'usuario', 'usuario_nombre', 'numero_cuenta', 'saldo']

class CuentaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Cuenta.objects.all()
    serializer_class = CuentaSerializer

    def get_queryset(self):
        # Solo las cuentas del usuario autenticado
        return Cuenta.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Asocia la cuenta al usuario autenticado
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post'], url_path='depositar')
    def depositar(self, request, pk=None):
        cuenta = self.get_object()
        monto_raw = request.data.get('monto')
        descripcion = request.data.get('descripcion', '')
        try:
            monto = Decimal(str(monto_raw))
            if monto <= 0:
                raise InvalidOperation
        except (InvalidOperation, TypeError):
            return Response({'error': 'Monto inválido'}, status=status.HTTP_400_BAD_REQUEST)

        cuenta.saldo = cuenta.saldo + monto
        cuenta.save()

        Movimiento.objects.create(
            cuenta=cuenta,
            tipo='INGRESO',
            monto=monto,
            descripcion=descripcion
        )
        return Response(self.get_serializer(cuenta).data)

    @action(detail=True, methods=['post'], url_path='retirar')
    def retirar(self, request, pk=None):
        cuenta = self.get_object()
        monto_raw = request.data.get('monto')
        descripcion = request.data.get('descripcion', '')
        try:
            monto = Decimal(str(monto_raw))
            if monto <= 0 or monto > cuenta.saldo:
                raise InvalidOperation
        except (InvalidOperation, TypeError):
            return Response({'error': 'Monto inválido o saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)


        cuenta.saldo = cuenta.saldo - monto
        cuenta.save()

        Movimiento.objects.create(
            cuenta=cuenta,
            tipo='EGRESO',
            monto=monto,
            descripcion=descripcion
        )
        return Response(self.get_serializer(cuenta).data)

    @action(detail=True, methods=['post'], url_path='transferir')
    def transferir(self, request, pk=None):
        try:
            origen = self.get_object()
        except Http404:
            return Response({'error': 'Cuenta origen no encontrada o no pertenece al usuario autenticado'},
                            status=status.HTTP_404_NOT_FOUND)

        destino_num = request.data.get('numero_cuenta', '').strip()
        monto_raw = request.data.get('monto')
        descripcion = request.data.get('descripcion', '')

        print(f"Transferencia solicitada: origen {origen.numero_cuenta} -> destino {destino_num}, monto: {monto_raw}")

        #cuenta destino tenga 10 dígitos
        if not destino_num.isdigit() or len(destino_num) != 10:
            return Response({'error': 'Número de cuenta destino inválido'}, status=status.HTTP_400_BAD_REQUEST)

        # Validar cuenta destino (en toda la base, no solo del usuario)
        try:
            cuenta_destino = Cuenta.objects.get(numero_cuenta=destino_num)
        except Cuenta.DoesNotExist:
            return Response({'error': 'Cuenta destino no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        # Validar monto
        try:
            monto = Decimal(str(monto_raw))
            if monto <= 0 or monto > origen.saldo:
                raise InvalidOperation
        except (InvalidOperation, TypeError):
            return Response({'error': 'Monto inválido o saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

        # Procesar transferencia
        origen.saldo -= monto
        origen.save()
        Movimiento.objects.create(
            cuenta=origen,
            tipo='TRANSFERENCIA_ENVIADA',
            monto=monto,
            descripcion=f"A {cuenta_destino.numero_cuenta} - {descripcion}"
        )

        cuenta_destino.saldo += monto
        cuenta_destino.save()
        Movimiento.objects.create(
            cuenta=cuenta_destino,
            tipo='TRANSFERENCIA_RECIBIDA',
            monto=monto,
            descripcion=f"De {origen.numero_cuenta} - {descripcion}"
        )

        return Response(self.get_serializer(origen).data)