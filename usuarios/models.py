from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

ROLES = (
    ('no asignado', 'No Asignado'),
    ('residente', 'Residente'),
    ('encargado', 'Encargado'),
    ('seguridad', 'Seguridad'),
    ('administrador', 'Administrador'),  # Nuevo rol
)

class UsuarioPersonalizado(AbstractUser):
    # Validadores personalizados
    solo_letras = RegexValidator(
        r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$',
        'Solo se permiten letras y espacios'
    )
    
    email_validator = RegexValidator(
        r'^[a-zA-Z0-9._%+-]+@uab\.edu\.bo$',
        'El correo debe ser del dominio @uab.edu.bo'
    )

    # Campos personalizados
    first_name = models.CharField(
        'nombre',
        max_length=150,
        validators=[solo_letras]
    )
    last_name = models.CharField(
        'apellido',
        max_length=150,
        validators=[solo_letras]
    )
    email = models.EmailField(
        'correo electrónico',
        unique=True,
        validators=[email_validator]
    )
    tipo_usuario = models.CharField(
        max_length=20,
        choices=ROLES,
        default='no asignado'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def clean(self):
        super().clean()
        if len(self.password) < 6:
            raise ValidationError('La contraseña debe tener al menos 6 caracteres')

    def __str__(self):
        return f"{self.email} ({self.tipo_usuario})"