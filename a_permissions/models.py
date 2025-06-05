from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericRelation
from a_audit.models import AuditLog
from django.utils import timezone
from a_users.models import User

class Permission(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('APPROVED', 'Aprobado'),
        ('REJECTED', 'Rechazado'),
        ('COMPLETED', 'Completado'),
        ('CANCELLED', 'Cancelado'),
    ]
    
    resident = models.ForeignKey(
        User,
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
        'Estado',
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    
    # Campos de auditoría
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de actualización', auto_now=True)
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

    @classmethod
    def has_active_permission(cls, resident):
        """
        Verifica si un residente tiene un permiso activo (pendiente o aprobado y no vencido)
        """
        now = timezone.now()
        return cls.objects.filter(
            resident=resident,
            status__in=['PENDING', 'APPROVED'],
            end_date__gt=now
        ).exists()

    def is_active(self):
        """
        Verifica si el permiso está activo (no completado, no cancelado, no rechazado y no vencido)
        """
        now = timezone.now()
        return (
            self.status in ['PENDING', 'APPROVED'] and
            self.end_date > now
        )


#eliminar estos campos 

# start_date = models.DateTimeField('Fecha de inicio')
# end_date = models.DateTimeField('Fecha de fin')