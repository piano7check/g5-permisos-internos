from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Permission
from .forms import PermissionForm
import json
from django.db.models import Q

# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

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

class PermissionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Permission
    template_name = 'permissions/permission_list.html'
    context_object_name = 'permissions'
    paginate_by = 20

    def test_func(self):
        return self.request.user.role == 'ENCARGADO'

    def get_queryset(self):
        queryset = Permission.objects.filter(
            resident__controlled_area=self.request.user.controlled_area
        ).select_related('resident', 'approver')

        # Filtro por estado
        status = self.request.GET.get('status')
        if status in ['PENDING', 'APPROVED', 'REJECTED', 'COMPLETED']:
            queryset = queryset.filter(status=status)
        else:
            # Por defecto mostrar pendientes primero
            queryset = queryset.filter(status='PENDING')

        # Filtro por fecha
        date = self.request.GET.get('date')
        if date:
            queryset = queryset.filter(
                Q(start_date__date=date) | 
                Q(end_date__date=date)
            )

        # Ordenar por estado y fecha
        return queryset.order_by(
            'status',
            '-created_at'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Permission.STATUS_CHOICES
        return context
