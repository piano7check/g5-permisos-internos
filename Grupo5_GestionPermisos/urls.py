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
from django.views.generic import RedirectView
from django.shortcuts import redirect
from a_core.views import HomeView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Autenticación - Redirigir todo a Google OAuth
    path('accounts/login/', RedirectView.as_view(url='/accounts/google/login/', permanent=True), name='account_login'),
    path('accounts/signup/', RedirectView.as_view(url='/accounts/google/login/', permanent=True), name='account_signup'),
    path('accounts/3rdparty/signup/', RedirectView.as_view(url='/accounts/google/login/', permanent=True)),
    path('accounts/', include('allauth.urls')),
    
    # Redirigir /login/ a /accounts/login/
    path('login/', lambda request: redirect('account_login', permanent=True)),
    
    # Apps del proyecto
    path('users/', include('a_users.urls')),
    path('permissions/', include('a_permissions.urls')),
    path('security/', include('a_security.urls')),
    #para que me muestre la vista de inicio
    # Página principal
    #path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
]
#
# Personalizar títulos del admin
admin.site.site_header = 'Administración del Sistema de Permisos'
admin.site.site_title = 'Admin Permisos'
admin.site.index_title = 'Panel de Administración'
