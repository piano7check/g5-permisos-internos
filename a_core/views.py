from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from a_permissions.models import Permission
from a_permissions.forms import PermissionForm

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        # No redirección automática, solo mostrar home
        return super().get(request, *args, **kwargs)

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
