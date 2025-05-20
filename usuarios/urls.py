from django.urls import path, include
from .views import residente_home, vista_home, redireccion_por_rol, encargado_home, seguridad_home, login_google

urlpatterns = [
    path('', vista_home, name='home'),
    path('login/', login_google, name='login_google'),
    # Solo Google login/registro
    path('redireccion/', redireccion_por_rol, name='redireccion_por_rol'),
    path('residente/', residente_home, name='residente_home'),    
    path('encargado/', encargado_home, name='encargado_home'),
    path('seguridad/', seguridad_home, name='seguridad_home'),
    # Google social login
    path('accounts/', include('allauth.urls')),
]