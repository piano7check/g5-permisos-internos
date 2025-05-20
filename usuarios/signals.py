from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import UsuarioPersonalizado

@receiver(post_save, sender=UsuarioPersonalizado)
def asignar_permisos_usuario(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff and not instance.is_superuser:
            content_type = ContentType.objects.get_for_model(type(instance))
            perms = Permission.objects.filter(content_type=content_type)
            instance.user_permissions.set(perms)
        else:
            instance.user_permissions.clear()
