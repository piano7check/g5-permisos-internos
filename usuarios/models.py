from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import CustomValidators

ROLES = (
    ('no asignado', 'No Asignado'),
    ('residente', 'Residente'),
    ('encargado', 'Encargado'),
    ('seguridad', 'Seguridad'),
    ('administrador', 'Administrador'),  # Nuevo rol
)

class UsuarioPersonalizado(AbstractUser):
    first_name = models.CharField(
        'nombre',
        max_length=150,
        validators=[CustomValidators.solo_letras()]
    )
    last_name = models.CharField(
        'apellido',
        max_length=150,
        validators=[CustomValidators.solo_letras()]
    )
    email = models.EmailField(
        'correo electrónico',
        unique=True,
        validators=[CustomValidators.email_uab()]
    )
    tipo_usuario = models.CharField(
        max_length=20,
        choices=ROLES,
        default='no asignado'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return f"{self.email} ({self.tipo_usuario})"