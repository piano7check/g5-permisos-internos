from django.utils import timezone
from a_permissions.models import Permission
from datetime import timedelta

def notificar_permisos_proximos_a_vencer():
    ahora = timezone.now()
    margen_aviso = timedelta(minutes=15)  # Puedes cambiar esto a 30 o 60 si prefieres
    tiempo_limite = ahora + margen_aviso

    permisos = Permission.objects.filter(
        status='APPROVED',
        end_date__gt=ahora,
        end_date__lte=tiempo_limite,
        notified=False
    )

    for permiso in permisos:
        residente = permiso.resident
        print(f"🔔 Notificación: El permiso de {residente.email} está por vencer (Fin: {permiso.end_date})")

        # Marcar como notificado
        permiso.notified = True
        permiso.save()
