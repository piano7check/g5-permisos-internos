from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from a_permissions.models import Permission

# Create your views here.

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        if request.user.role == 'RESIDENTE':
            return super().get(request, *args, **kwargs)
        elif request.user.role == 'ENCARGADO':
            return redirect('permissions:permission_list')
        elif request.user.role == 'SEGURIDAD':
            return redirect('security:register_access')
        elif request.user.role == 'ADMIN':
            return super().get(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
