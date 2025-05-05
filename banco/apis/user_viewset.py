from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from banco.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id',  'nombre_completo', 'ci','username', 'password')


class UsuarioRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ( 'nombre_completo', 'ci','username', 'password')

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'register':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(methods=['post'], detail=False, url_path='register')
    def register(self, request):
        serializer = UsuarioRegisterSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            return Response({
                'id': usuario.id,
                'username': usuario.username
            }, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        usuario = request.user
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
