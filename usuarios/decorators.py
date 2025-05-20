from django.shortcuts import redirect
from functools import wraps

def rol_requerido(rol):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.tipo_usuario != rol:
                return redirect('redireccion_por_rol')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
