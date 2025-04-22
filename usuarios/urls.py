from django.urls import path
from .views import UsuarioCreateView, UsuarioListView, vista_registro, vista_home, vista_login

urlpatterns = [
    path('', vista_home, name='home'),
    path('register/', vista_registro, name='register'),
    path('api/registro/', UsuarioCreateView.as_view(), name='api_registro'),
    path('api/listar/', UsuarioListView.as_view(), name='listar_usuarios'),
    path('login/', vista_login, name='login'),
    
]