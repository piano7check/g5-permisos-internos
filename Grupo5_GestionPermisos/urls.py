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
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from a_core.views import HomeRedirectView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('redir/', HomeRedirectView.as_view(), name='home_redirect'),
    path('admin', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('permissions/', include('a_permissions.urls')),
    path('security/', include('a_security.urls')),
    path('users/', include('a_users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Personalizar títulos del admin
admin.site.site_header = 'Administración del Sistema de Permisos'
admin.site.site_title = 'Admin Permisos'
admin.site.index_title = 'Panel de Administración'
