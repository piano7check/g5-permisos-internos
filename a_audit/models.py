from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class AuditLog(models.Model):
    class ActionType(models.TextChoices):
        PERMISSION_APPROVED = 'PERMISSION_APPROVED', 'Permiso Aprobado'
        PERMISSION_REJECTED = 'PERMISSION_REJECTED', 'Permiso Rechazado'
        ACCESS_ENTRY = 'ACCESS_ENTRY', 'Registro de Entrada'
        ACCESS_EXIT = 'ACCESS_EXIT', 'Registro de Salida'
    
    # Quién realizó la acción
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='audit_logs',
        verbose_name='Usuario que realizó la acción'
    )
    
    # Tipo de acción realizada
    action_type = models.CharField(
        'Tipo de Acción',
        max_length=50,
        choices=ActionType.choices
    )
    
    # Fecha y hora de la acción
    timestamp = models.DateTimeField(
        'Fecha y Hora',
        auto_now_add=True
    )
    
    # Detalles adicionales de la acción
    details = models.TextField(
        'Detalles',
        blank=True
    )
    
    # Campos para la referencia genérica al objeto afectado
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Tipo de Contenido'
    )
    object_id = models.PositiveIntegerField('ID del Objeto')
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # IP desde donde se realizó la acción
    ip_address = models.GenericIPAddressField(
        'Dirección IP',
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = 'Registros de Auditoría'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_action_type_display()} - {self.timestamp}"
