from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from a_audit.models import AuditLog

class Permission(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('APPROVED', 'Aprobado'),
        ('REJECTED', 'Rechazado'),
        ('COMPLETED', 'Completado'),
    ]
    
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='permissions',
        limit_choices_to={'role': 'RESIDENTE'},
        verbose_name='Residente'
    )
    
    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='permissions_approved',
        limit_choices_to={'role': 'ENCARGADO'}
    )
    
    # Detalles del permiso
    reason = models.TextField('Motivo')
    start_date = models.DateTimeField('Fecha de inicio')
    end_date = models.DateTimeField('Fecha de fin')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField('Motivo de rechazo', blank=True)
    
    # Relación con el log de auditoría
    audit_logs = GenericRelation(AuditLog)
    
    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Permiso de {self.resident.get_full_name()} - {self.get_status_display()}"
    
    def clean(self):
        # Validar que el encargado sea del área correspondiente
        if self.approver and self.resident:
            if self.approver.controlled_area != self.resident.controlled_area:
                raise ValidationError({
                    'approver': 'El encargado debe ser del mismo área que el residente'
                })
        
        # Validar fechas
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError({
                'end_date': 'La fecha de fin no puede ser anterior a la fecha de inicio'
            })
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
