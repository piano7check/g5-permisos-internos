"""
URL configuration for Grupo5_GestionPermisos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from a_core.views import HomeView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Autenticación
    path('accounts/', include('allauth.urls')),
    
    # Apps del proyecto
    path('users/', include('a_users.urls')),
    path('permissions/', include('a_permissions.urls')),
    path('security/', include('a_security.urls')),
    
    # Página principal
    path('', HomeView.as_view(), name='home'),
]

# Personalizar títulos del admin
admin.site.site_header = 'Administración del Sistema de Permisos'
admin.site.site_title = 'Admin Permisos'
admin.site.index_title = 'Panel de Administración'
