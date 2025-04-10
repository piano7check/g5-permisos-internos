import json
import bcrypt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from .models import UsuarioPersonalizado
import re
# API - POST /users
@csrf_exempt
def crear_usuario(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        datos = json.loads(request.body)
        nombre = datos.get('nombre')
        apellido = datos.get('apellido')
        email = datos.get('email')
        password = datos.get('password')

        # Validaciones
        # Validación de formato de nombre
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$', nombre):
            return JsonResponse({'error': 'El nombre solo puede contener letras.'}, status=400)

        # Validación de formato de apellido
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$', apellido):
            return JsonResponse({'error': 'El apellido solo puede contener letras.'}, status=400)
        
        if not nombre or not apellido or not email or not password:
            return JsonResponse({'error': 'Todos los campos son obligatorios.'}, status=400)

        if UsuarioPersonalizado.objects.filter(email=email).exists():
            return JsonResponse({'error': 'El email ya está en uso.'}, status=409)

        if len(password) < 6:
            return JsonResponse({'error': 'La contraseña debe tener al menos 6 caracteres.'}, status=400)

        # Hash de contraseña
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # Crear usuario
        usuario = UsuarioPersonalizado.objects.create(
            username=email.split('@')[0],
            email=email,
            first_name=nombre,
            last_name=apellido,
            password=password_hash,
            tipo_usuario='no asignado'
        )

        # Enviar correo
        send_mail(
            'Registro Exitoso',
            f'Hola {nombre} {apellido}, tu cuenta fue registrada correctamente.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return JsonResponse({
            'id': usuario.id,
            'nombre': usuario.first_name,
            'apellido': usuario.last_name,
            'email': usuario.email,
            'tipo_usuario': usuario.tipo_usuario
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)
        
    

# HTML - GET /registro
def vista_registro(request):
    return render(request, 'usuarios/register.html')
