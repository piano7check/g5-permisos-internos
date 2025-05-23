from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate

def configure_default_site(sender, **kwargs):
    """
    Configurar el sitio por defecto después de que las migraciones se hayan completado
    """
    try:
        from django.contrib.sites.models import Site
        site = Site.objects.get(id=settings.SITE_ID)
        site.domain = settings.LOCAL_DOMAIN
        site.name = 'Permisos Internos'
        site.save()
    except Exception as e:
        print(f"No se pudo configurar el sitio: {e}")

class ACoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'a_core'

    def ready(self):
        """
        Configuración que se ejecuta cuando la aplicación está lista
        """
        post_migrate.connect(configure_default_site, sender=self)
