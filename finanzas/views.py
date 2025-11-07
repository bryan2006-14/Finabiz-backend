from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.db import IntegrityError
from .models import Usuario
import json

@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_usuario(request):
    """API para registrar usuario desde PHP"""
    try:
        data = request.data
        
        # Validar datos requeridos
        if not all([data.get('nombre'), data.get('correo'), data.get('password')]):
            return Response({
                'success': False,
                'message': 'Todos los campos son obligatorios'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear usuario
        usuario = Usuario.objects.create_user(
            correo=data['correo'],
            password=data['password'],
            nombre=data['nombre']
        )
        
        return Response({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'user': {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'correo': usuario.correo
            }
        })
        
    except IntegrityError:
        return Response({
            'success': False,
            'message': 'El correo ya está registrado'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error del servidor: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_usuario(request):
    """API para login desde PHP"""
    try:
        correo = request.data.get('correo')
        password = request.data.get('password')
        
        if not correo or not password:
            return Response({
                'success': False,
                'message': 'Correo y contraseña son obligatorios'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        usuario = authenticate(request, correo=correo, password=password)
        
        if usuario is not None:
            return Response({
                'success': True,
                'message': 'Login exitoso',
                'user': {
                    'id': usuario.id,
                    'nombre': usuario.nombre,
                    'correo': usuario.correo,
                    'foto_perfil': usuario.foto_perfil
                }
            })
        else:
            # Verificar si el usuario existe pero la contraseña es incorrecta
            try:
                usuario_existente = Usuario.objects.get(correo=correo)
                return Response({
                    'success': False,
                    'message': 'Contraseña incorrecta'
                }, status=status.HTTP_401_UNAUTHORIZED)
            except Usuario.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'No existe un usuario con este correo'
                }, status=status.HTTP_404_NOT_FOUND)
            
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error del servidor: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def obtener_usuarios(request):
    """API para obtener lista de usuarios (solo para testing)"""
    try:
        usuarios = Usuario.objects.all()
        usuarios_data = []
        
        for usuario in usuarios:
            usuarios_data.append({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'correo': usuario.correo,
                'foto_perfil': usuario.foto_perfil
            })
        
        return Response({
            'success': True,
            'usuarios': usuarios_data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """API para verificar que el servidor está funcionando"""
    return Response({
        'status': 'ok',
        'message': 'Django server is running',
        'app': 'Finabiz Backend'
    })