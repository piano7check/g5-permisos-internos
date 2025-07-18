from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from a_permissions.models import Permission
from a_permissions.forms import PermissionForm
from django.views import View
from django.urls import reverse

# Create your views here.

class HomeRedirectView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if hasattr(user, 'is_encargado') and user.is_encargado:
                return redirect('permissions:pending')
            elif hasattr(user, 'is_seguridad') and user.is_seguridad:
                return redirect('security:register_access')
            elif hasattr(user, 'is_residente') and user.is_residente:
                form = PermissionForm()
                return render(request, 'home.html', {'form': form})
        # Si no está autenticado, mostrar la página de bienvenida
        return render(request, 'home.html')

class HomeView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        # Si el usuario está autenticado y no es residente, redirigir a la lógica de redirección por rol
        if request.user.is_authenticated and not (hasattr(request.user, 'is_residente') and request.user.is_residente):
            return redirect(reverse('home_redirect'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and self.request.user.is_residente:
            context['form'] = PermissionForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_residente:
            messages.error(request, 'No tienes permiso para realizar esta acción.')
            return redirect('home')

        # Verificar si ya tiene un permiso activo
        if Permission.has_active_permission(request.user):
            messages.error(
                request,
                'Ya tienes un permiso activo. Debes esperar a que se complete para solicitar uno nuevo.'
            )
            return redirect('home')

        form = PermissionForm(request.POST)
        if form.is_valid():
            permission = form.save(commit=False)
            permission.resident = request.user
            permission.save()
            messages.success(
                request,
                'Tu solicitud de permiso ha sido enviada y está pendiente de aprobación.'
            )
            return redirect('permissions:my_permissions')
        
        return self.render_to_response({'form': form})
