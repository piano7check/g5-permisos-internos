from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Permission
import json

# Create your views here.

class PermissionRequestView(LoginRequiredMixin, CreateView):
    model = Permission
    template_name = 'permissions/request.html'
    fields = ['reason', 'start_date', 'end_date']
    success_url = reverse_lazy('permissions:my_permissions')

    def form_valid(self, form):
        form.instance.resident = self.request.user
        messages.success(self.request, 'Tu solicitud de permiso ha sido enviada.')
        return super().form_valid(form)

class MyPermissionsView(LoginRequiredMixin, ListView):
    template_name = 'permissions/my_permissions.html'
    model = Permission
    context_object_name = 'permissions'

    def get_queryset(self):
        return Permission.objects.filter(resident=self.request.user)

class PendingPermissionsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'permissions/pending.html'
    model = Permission
    context_object_name = 'permissions'

    def test_func(self):
        return self.request.user.is_encargado

    def get_queryset(self):
        return Permission.objects.filter(
            status='PENDING',
            resident__controlled_area=self.request.user.controlled_area
        )

class PermissionHistoryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'permissions/history.html'
    model = Permission
    context_object_name = 'permissions'

    def test_func(self):
        return self.request.user.is_encargado

    def get_queryset(self):
        return Permission.objects.filter(
            resident__controlled_area=self.request.user.controlled_area
        ).exclude(status='PENDING')

class PermissionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'permissions/detail.html'
    model = Permission
    context_object_name = 'permission'

    def get_queryset(self):
        if self.request.user.is_encargado:
            return Permission.objects.filter(
                resident__controlled_area=self.request.user.controlled_area
            )
        return Permission.objects.filter(resident=self.request.user)

class ApprovePermissionView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_encargado

    def post(self, request, pk):
        permission = get_object_or_404(
            Permission,
            pk=pk,
            status='PENDING',
            resident__controlled_area=request.user.controlled_area
        )
        
        permission.status = 'APPROVED'
        permission.approver = request.user
        permission.approval_date = timezone.now()
        permission.save()
        
        # Aquí podrías enviar un correo electrónico al residente
        
        return JsonResponse({'status': 'success'})

class RejectPermissionView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_encargado

    def post(self, request, pk):
        permission = get_object_or_404(
            Permission,
            pk=pk,
            status='PENDING',
            resident__controlled_area=request.user.controlled_area
        )
        
        data = json.loads(request.body)
        rejection_reason = data.get('rejection_reason')
        
        if not rejection_reason:
            return JsonResponse({'status': 'error', 'message': 'Se requiere un motivo de rechazo'}, status=400)
        
        permission.status = 'REJECTED'
        permission.approver = request.user
        permission.approval_date = timezone.now()
        permission.rejection_reason = rejection_reason
        permission.save()
        
        # Aquí podrías enviar un correo electrónico al residente
        
        return JsonResponse({'status': 'success'})
