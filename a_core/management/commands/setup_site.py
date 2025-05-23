from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Configura el sitio por defecto para autenticación social'

    def handle(self, *args, **kwargs):
        # Actualizar el sitio por defecto
        site = Site.objects.get(id=1)
        site.domain = '127.0.0.1:8000'
        site.name = 'Sistema de Permisos'
        site.save()
        
        self.stdout.write(
            self.style.SUCCESS('Sitio configurado correctamente')
        ) 