from django.urls import path
from . import views

urlpatterns = [
    path('api/registrar/', views.registrar_usuario, name='registrar'),
    path('api/login/', views.login_usuario, name='login'),
    path('api/usuarios/', views.obtener_usuarios, name='obtener_usuarios'),
    path('api/health/', views.health_check, name='health_check'),
]