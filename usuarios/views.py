from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import UsuarioPersonalizado
from .serializers import UsuarioPersonalizadoSerializer
from .email_service import enviar_correo_registro

class UsuarioCreateView(APIView):
    def post(self, request):
        serializer = UsuarioPersonalizadoSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()

            # Enviar correo después de guardar
            enviar_correo_registro(
                usuario.first_name,
                usuario.last_name,
                usuario.email
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuarioListView(APIView):
    def get(self, request):
        usuarios = UsuarioPersonalizado.objects.all()
        serializer = UsuarioPersonalizadoSerializer(usuarios, many=True)
        return Response(serializer.data)

# HTML - GET /
def vista_registro(request):
    return render(request, 'usuarios/register.html')

def vista_home(request):
    return render(request, 'usuarios/home.html')

def vista_login(request):
    return render(request, 'usuarios/login.html')
