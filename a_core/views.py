from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from a_permissions.models import Permission

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Si el usuario está autenticado y es residente, obtener sus últimos permisos
        if self.request.user.is_authenticated and self.request.user.is_residente:
            context['recent_permissions'] = Permission.objects.filter(
                resident=self.request.user
            ).order_by('-created_at')[:5]
        
        return context
