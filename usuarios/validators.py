from django.core.validators import RegexValidator
import re

class CustomValidators:
    @staticmethod
    def solo_letras():
        return RegexValidator(
            r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$',
            'Solo se permiten letras y espacios.'
        )

    @staticmethod
    def email_uab():
        return RegexValidator(
            r'^[a-zA-Z0-9._%+-]+@uab\.edu\.bo$',
            'El correo debe ser del dominio @uab.edu.bo.'
        )


class CustomUserdValidator:

    @staticmethod
    def validar_email_campos_llenos( nombre, apellido, email, password):
        # Verifica si todos los campos están presentes
        if not nombre or not apellido or not email or not password:
            return 'Todos los campos son obligatorios.'

        return None
    
    @staticmethod
    def validar_nombre_apellido(nombre, apellido):
        # Nombre y apellido con solo letras
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$', nombre):
            return 'El nombre solo puede contener letras.'
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$', apellido):
            return 'El apellido solo puede contener letras.'

        return None
    
    @staticmethod
    def validar_email(email):
        # Email debe ser del dominio correcto
        if not email.endswith('@uab.edu.bo'):
            return 'El correo debe terminar en @uab.edu.bo.'

        return None

    @staticmethod
    def validar_contrasena(password):
        # Validación de longitud de contraseña
        if len(password) < 6:
            return 'La contraseña debe tener al menos 6 caracteres.'

        return None

    @staticmethod
    def validar_email_existente(email):
        from .models import UsuarioPersonalizado
        # Verifica si el correo ya existe en la base de datos
        if UsuarioPersonalizado.objects.filter(email=email).exists():
            return 'El correo ya está registrado.'

        return None


    
    