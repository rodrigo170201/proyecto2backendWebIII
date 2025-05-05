from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated

from banco.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'nombre_completo', 'ci', 'password']

class UsuarioViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer