from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from a_permissions.models import Permission

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        # No redirección automática, solo mostrar home
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Puedes agregar más contexto si lo necesitas
        return context
