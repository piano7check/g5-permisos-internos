from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import User
from .forms import UserProfileForm

# Create your views here.

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_residente:
            # Agregar estadísticas de permisos
            permissions = self.request.user.permissions.all()
            context['total_permissions'] = permissions.count()
            context['approved_permissions'] = permissions.filter(status='APPROVED').count()
            context['pending_permissions'] = permissions.filter(status='PENDING').count()
        return context
