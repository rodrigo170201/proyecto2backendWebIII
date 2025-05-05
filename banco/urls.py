from django.urls import path, include
from rest_framework import routers

from banco.apis import CuentaViewSet, UsuarioViewSet, MovimientoViewSet, BeneficiarioViewSet
from banco.apis.user_viewset import UserViewSet

router = routers.DefaultRouter()
router.register('cuenta', CuentaViewSet)
router.register('usuario', UsuarioViewSet)
router.register('movimiento', MovimientoViewSet)
router.register('beneficiario', BeneficiarioViewSet)

router.register("auth", UserViewSet, basename="auth")

urlpatterns = [
    path('',include(router.urls)),
]