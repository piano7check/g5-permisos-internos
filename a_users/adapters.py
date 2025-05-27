from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.shortcuts import redirect
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth import get_user_model, login as auth_login
from allauth.account.utils import user_email, user_username
from django.urls import reverse

User = get_user_model()

def split_full_name(full_name):
    """
    Función para dividir el nombre completo en nombre y apellido.
    Para el formato "Apellidos Nombres", divide en la última ocurrencia de espacio.
    """
    if not full_name:
        return '', ''
    
    # Dividir el nombre completo
    parts = full_name.split()
    if len(parts) <= 1:
        return full_name, ''
    

    # Asumimos que los primeros términos son apellidos y los últimos son nombres
    # Encontrar el punto medio (asumiendo que hay al menos un apellido y un nombre)
    mid_point = len(parts) // 2
    
    # Unir los apellidos y nombres
    last_name = ' '.join(parts[:mid_point])
    first_name = ' '.join(parts[mid_point:])
    
    return first_name, last_name

class NoNewUsersAccountAdapter(DefaultAccountAdapter):
    """
    Adaptador que deshabilita el registro tradicional y solo permite login con Google
    """
    def is_open_for_signup(self, request):
        return False

    def login(self, request, user):
        auth_login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
        return redirect(self.get_login_redirect_url(request))

    def get_login_redirect_url(self, request):
        """
        URL a la que redirigir después del login exitoso
        """
        return settings.LOGIN_REDIRECT_URL

    def save_user(self, request, user, form, commit=True):
        """
        Este método es llamado cuando se crea un nuevo usuario. Aseguramos que
        el email esté configurado correctamente.
        """
        data = form.cleaned_data if form else {}
        email = data.get('email') or user_email(user) or ''
        user_email(user, email)
        user_username(user, email)
        
        if commit:
            user.save()
        return user

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        """
        Determina si un usuario puede registrarse usando autenticación social.
        """
        return True

    def pre_social_login(self, request, sociallogin):
        """
        Intercepta el proceso de login social antes de que ocurra.
        Verifica el dominio institucional y maneja usuarios existentes.
        """
        email = sociallogin.account.extra_data.get('email')
        if not email:
            raise ImmediateHttpResponse(
                redirect('/accounts/google/login/?error=email_required')
            )
        
        # Verificar dominio institucional
        if not email.endswith('@uab.edu.bo'):
            raise ImmediateHttpResponse(
                redirect('/accounts/google/login/?error=invalid_domain&prompt=select_account')
            )
        
        try:
            user = User.objects.get(email=email)
            sociallogin.connect(request, user)
            auth_login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
            raise ImmediateHttpResponse(redirect('/'))
        except User.DoesNotExist:
            pass

    def populate_user(self, request, sociallogin, data):
        """
        Personaliza la creación del usuario cuando se registra con Google.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Obtener datos del perfil de Google
        email = data.get('email', '')
        full_name = data.get('name', '')  # Obtener el nombre completo
        
        # Dividir el nombre completo en nombre y apellido
        first_name, last_name = split_full_name(full_name)
        
        # Configurar campos del usuario directamente
        user.email = email
        user.username = email
        user.first_name = first_name
        user.last_name = last_name
        user.role = 'RESIDENTE'
        
        # Si el dominio es uab.edu.bo, asumimos que es un usuario institucional
          # Opcional: dar acceso al admin
        

    def save_user(self, request, sociallogin, form=None):
        """
        Guarda el usuario y maneja el proceso de login.
        """
        user = super().save_user(request, sociallogin, form)
        
        # Obtener y actualizar datos del usuario
        email = sociallogin.account.extra_data.get('email', '')
        full_name = sociallogin.account.extra_data.get('name', '')
        
        if full_name:
            first_name, last_name = split_full_name(full_name)
            user.first_name = first_name
            user.last_name = last_name
        
        user.email = email
        user.username = email
        user.save()
        
        auth_login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
        raise ImmediateHttpResponse(redirect('/'))

    def get_connect_redirect_url(self, request, socialaccount):
        """
        URL a la que redirigir después de conectar una cuenta social
        """
        return '/' 