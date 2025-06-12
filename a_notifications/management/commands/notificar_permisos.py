from django.core.management.base import BaseCommand
from a_notifications.tasks import notificar_permisos_proximos_a_vencer

class Command(BaseCommand):
    help = "Notifica a los internos cuando su permiso está por vencer"

    def handle(self, *args, **kwargs):
        self.stdout.write("🔄 Ejecutando notificación de permisos próximos a vencer...")
        notificar_permisos_proximos_a_vencer()
        self.stdout.write("✅ Notificaciones procesadas.")
