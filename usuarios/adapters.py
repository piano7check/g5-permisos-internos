from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import UsuarioPersonalizado

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        # Solo asignar tipo_usuario, no accedas a relaciones M2M ni guardes aquí
        try:
            existing = UsuarioPersonalizado.objects.get(email=user.email)
            user.tipo_usuario = existing.tipo_usuario
        except UsuarioPersonalizado.DoesNotExist:
            user.tipo_usuario = 'residente'  # Por defecto
        # Asegura username único para usuarios Google
        if not user.username:
            if user.email:
                user.username = user.email.split('@')[0]
            else:
                import uuid
                user.username = str(uuid.uuid4())
        return user

    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        is_new = user.pk is None
        user.save()  # Guarda primero para tener un id
        return super().save_user(request, sociallogin, form)
