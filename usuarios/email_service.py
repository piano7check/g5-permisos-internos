from django.core.mail import send_mail
from django.conf import settings

def enviar_correo_registro(nombre, apellido, email):
    asunto = 'Registro Exitoso'
    mensaje = f'Hola {nombre} {apellido}, tu cuenta fue registrada correctamente.'
    send_mail(asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False)
