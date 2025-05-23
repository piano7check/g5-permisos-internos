from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        ENCARGADO = 'ENCARGADO', 'Encargado'
        RESIDENTE = 'RESIDENTE', 'Residente'
        SEGURIDAD = 'SEGURIDAD', 'Seguridad'
    
    class Gender(models.TextChoices):
        MALE = 'M', 'Masculino'
        FEMALE = 'F', 'Femenino'
    
    class Area(models.TextChoices):
        MALE_RESIDENCE = 'MALE', 'Residencia Varones'
        FEMALE_RESIDENCE = 'FEMALE', 'Residencia Mujeres'
    
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.RESIDENTE
    )
    
    # Campos adicionales
    phone = models.CharField('Teléfono', max_length=15, blank=True)
    gender = models.CharField(
        'Género',
        max_length=1,
        choices=Gender.choices,
        null=True,
        blank=True
    )
    
    # Campo para controlar el área (solo para encargados y residentes)
    controlled_area = models.CharField(
        'Área',
        max_length=10,
        choices=Area.choices,
        null=True,
        blank=True,
        help_text='Área de residencia para residentes o área de control para encargados'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def save(self, *args, **kwargs):
        # Asignar área controlada según el rol y género
        if self.role == self.Roles.RESIDENTE and self.gender:
            # Para residentes, asignar según género
            self.controlled_area = self.Area.MALE_RESIDENCE if self.gender == self.Gender.MALE else self.Area.FEMALE_RESIDENCE
        elif self.role == self.Roles.SEGURIDAD:
            # Para seguridad, no asignar área controlada
            self.controlled_area = None
        # Para encargados, mantener el área asignada manualmente
        
        super().save(*args, **kwargs)
    
    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN
    
    @property
    def is_encargado(self):
        return self.role == self.Roles.ENCARGADO
    
    @property
    def is_residente(self):
        return self.role == self.Roles.RESIDENTE
    
    @property
    def is_seguridad(self):
        return self.role == self.Roles.SEGURIDAD
