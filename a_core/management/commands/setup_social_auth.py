from django.core.management.base import BaseCommand
from django.conf import settings
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Configura la autenticación social con Google OAuth'

    def handle(self, *args, **kwargs):
        # Asegurarse de que existe el sitio por defecto
        site, _ = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': settings.LOCAL_DOMAIN,
                'name': 'Sistema de Permisos'
            }
        )

        # Actualizar el dominio del sitio si es necesario
        if site.domain != settings.LOCAL_DOMAIN:
            site.domain = settings.LOCAL_DOMAIN
            site.save()

        # Crear o actualizar la aplicación social
        social_app, created = SocialApp.objects.update_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth',
                'client_id': settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID,
                'secret': settings.SOCIAL_AUTH_GOOGLE_SECRET,
                'key': ''
            }
        )

        # Asegurarse de que la aplicación está asociada al sitio
        social_app.sites.add(site)

        if created:
            self.stdout.write(
                self.style.SUCCESS('Aplicación social creada exitosamente')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Aplicación social actualizada exitosamente')
            ) 