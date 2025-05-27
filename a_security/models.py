from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from a_permissions.models import Permission
from a_audit.models import AuditLog
from django.utils import timezone

class AccessRecord(models.Model):
    ACCESS_TYPES = [
        ('ENTRY', 'Entrada'),
        ('EXIT', 'Salida'),
    ]

    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='access_records',
        limit_choices_to={'role': 'RESIDENTE'},
        verbose_name='Residente'
    )
    
    security_guard = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recorded_accesses',
        limit_choices_to={'role': 'SEGURIDAD'},
        verbose_name='Guardia de Seguridad'
    )
    
    timestamp = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha y Hora'
    )
    
    access_type = models.CharField(
        max_length=5,
        choices=ACCESS_TYPES,
        verbose_name='Tipo de Acceso'
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name='Observaciones'
    )
    
    permission = models.ForeignKey(
        'a_permissions.Permission',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='access_records',
        verbose_name='Permiso Asociado'
    )
    
    # Relación con el log de auditoría
    audit_logs = GenericRelation(AuditLog)
    
    class Meta:
        verbose_name = 'Registro de Acceso'
        verbose_name_plural = 'Registros de Acceso'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.get_access_type_display()} - {self.resident.get_full_name()} - {self.timestamp.strftime('%d/%m/%Y %H:%M')}"
    
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
        # Si es una entrada y hay un permiso activo, lo vinculamos
        if self.access_type == 'ENTRY' and not self.permission:
            active_permission = Permission.objects.filter(
                resident=self.resident,
                status='APPROVED',
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            ).first()
            if active_permission:
                self.permission = active_permission
        
        self.clean()
        super().save(*args, **kwargs)
