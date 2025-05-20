from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import rol_requerido

# Eliminar vistas y APIs de registro/login tradicionales, solo Google

def vista_home(request):
    return render(request, 'usuarios/home.html')

def login_google(request):
    return render(request, 'login_google.html')

@login_required
def redireccion_por_rol(request):
    user = request.user
    if user.tipo_usuario == 'residente':
        return redirect('residente_home')
    elif user.tipo_usuario == 'encargado':
        return redirect('encargado_home')
    elif user.tipo_usuario == 'seguridad':
        return redirect('seguridad_home')
    elif user.tipo_usuario == 'administrador':
        return redirect('/admin/')
    else:
        return redirect('home')

@rol_requerido('encargado')
def encargado_home(request):
    return render(request, 'usuarios/encargado_home.html')

@rol_requerido('seguridad')
def seguridad_home(request):
    return render(request, 'usuarios/seguridad_home.html')

@rol_requerido('residente')
def residente_home(request):
    return render(request, 'usuarios/residente_home.html')
