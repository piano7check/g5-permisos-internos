from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from a_permissions.models import Permission
from a_audit.models import AuditLog

class AccessRecord(models.Model):
    class RecordType(models.TextChoices):
        EXIT = 'EXIT', 'Salida'
        ENTRY = 'ENTRY', 'Entrada'
    
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name='access_records',
        limit_choices_to={'status': 'APPROVED'}
    )
    
    security_officer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recorded_accesses',
        limit_choices_to={'role': 'SEGURIDAD'}
    )
    
    record_type = models.CharField(
        'Tipo de Registro',
        max_length=10,
        choices=RecordType.choices
    )
    
    timestamp = models.DateTimeField('Fecha y Hora', auto_now_add=True)
    notes = models.TextField('Notas', blank=True)
    
    # Relación con el log de auditoría
    audit_logs = GenericRelation(AuditLog)
    
    class Meta:
        verbose_name = 'Registro de Acceso'
        verbose_name_plural = 'Registros de Acceso'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.get_record_type_display()} - {self.permission.resident.get_full_name()} - {self.timestamp}"
    
    def clean(self):
        # Validar que el permiso esté vigente
        if self.permission:
            if self.permission.status != 'APPROVED':
                raise ValidationError({
                    'permission': 'Solo se pueden registrar accesos para permisos aprobados'
                })
            
            if self.timestamp:
                if self.timestamp < self.permission.start_date or self.timestamp > self.permission.end_date:
                    raise ValidationError({
                        'timestamp': 'El registro debe estar dentro del período del permiso'
                    })
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
