from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from banco.models import Usuario, Beneficiario, Cuenta


class BeneficiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiario
        fields = ['id', 'usuario', 'nombre', 'numero_cuenta']
        read_only_fields = ['usuario']

class BeneficiarioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Beneficiario.objects.all()
    serializer_class = BeneficiarioSerializer

    def get_queryset(self):
        return Beneficiario.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)