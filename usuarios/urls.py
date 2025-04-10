from django.urls import path
from .views import crear_usuario, vista_registro

urlpatterns = [
    path('', vista_registro, name='vista_registro'),  # POST
    path('api/registro/', crear_usuario, name='api_registro'),
    
]