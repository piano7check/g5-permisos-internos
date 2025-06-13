from django.shortcuts import redirect
from django.urls import reverse

class ForceProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if (hasattr(request.user, 'is_residente') and request.user.is_residente) or \
               (hasattr(request.user, 'is_encargado') and request.user.is_encargado):
                if not request.user.gender and request.path not in [
                    reverse('users:profile'),
                    reverse('account_logout')
                ] and not request.path.startswith('/admin'):
                    return redirect('users:profile')
        return self.get_response(request) 