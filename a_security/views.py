from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import AccessRecord
from a_users.models import User
from a_permissions.models import Permission
import json
from django.db import models

# Create your views here.

class RegisterAccessView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'security/register_access.html'
    model = Permission
    context_object_name = 'permissions'
    paginate_by = 20

    def test_func(self):
        return self.request.user.role == 'SEGURIDAD'

    def get_queryset(self):
        queryset = Permission.objects.all().select_related('resident')

        # Filtro por estado
        status = self.request.GET.get('status')
        if status in ['PENDING', 'APPROVED', 'REJECTED', 'COMPLETED']:
            queryset = queryset.filter(status=status)
        else:
            # Por defecto mostrar los permisos activos y pendientes
            queryset = queryset.filter(
                Q(status='APPROVED') |
                Q(status='PENDING'),
                start_date__lte=timezone.now() + timezone.timedelta(days=1),  # Incluir permisos que empiezan en las próximas 24 horas
                end_date__gte=timezone.now()  # Solo permisos que no han expirado
            )

        # Filtro por área (opcional)
        area = self.request.GET.get('area')
        if area in ['MALE', 'FEMALE']:
            queryset = queryset.filter(resident__controlled_area=area)

        # Ordenar por estado y fecha
        return queryset.order_by(
            models.Case(
                models.When(status='APPROVED', then=0),
                models.When(status='PENDING', then=1),
                models.When(status='COMPLETED', then=2),
                models.When(status='REJECTED', then=3),
                default=4,
                output_field=models.IntegerField(),
            ),
            'start_date'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Permission.STATUS_CHOICES
        context['area_choices'] = [
            ('MALE', 'Residencia Varones'),
            ('FEMALE', 'Residencia Mujeres')
        ]
        
        # Obtener el último registro de acceso para cada permiso
        permissions_with_access = {}
        for permission in context['permissions']:
            last_access = AccessRecord.objects.filter(
                permission=permission
            ).order_by('-timestamp').first()
            permissions_with_access[permission.id] = last_access
        
        context['last_accesses'] = permissions_with_access
        return context

class AccessHistoryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'security/access_history.html'
    model = AccessRecord
    context_object_name = 'access_records'
    paginate_by = 50

    def test_func(self):
        return self.request.user.role == 'SEGURIDAD'

    def get_queryset(self):
        queryset = AccessRecord.objects.filter(
            resident__controlled_area=self.request.user.controlled_area
        ).select_related('resident', 'security_guard', 'permission')

        # Filtros por fecha
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from:
            queryset = queryset.filter(timestamp__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(timestamp__date__lte=date_to)

        # Filtro por tipo de acceso
        access_type = self.request.GET.get('access_type')
        if access_type in ['ENTRY', 'EXIT']:
            queryset = queryset.filter(access_type=access_type)

        # Filtro por residente
        resident_id = self.request.GET.get('resident')
        if resident_id:
            queryset = queryset.filter(resident_id=resident_id)

        return queryset.order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['residents'] = User.objects.filter(
            role='RESIDENTE',
            controlled_area=self.request.user.controlled_area
        )
        return context

class RecordAccessView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'SEGURIDAD'

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            permission_id = data.get('permission_id')
            access_type = data.get('access_type')
            notes = data.get('notes', '')

            permission = get_object_or_404(
                Permission,
                id=permission_id,
                status='APPROVED'
            )

            # Crear el registro de acceso
            access_record = AccessRecord.objects.create(
                resident=permission.resident,
                security_guard=request.user,
                access_type=access_type,
                notes=notes,
                permission=permission
            )

            # Si es una entrada y ya había una salida previa, marcar como completado
            if access_type == 'ENTRY':
                previous_exit = AccessRecord.objects.filter(
                    permission=permission,
                    access_type='EXIT'
                ).exists()
                
                if previous_exit:
                    permission.status = 'COMPLETED'
                    permission.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Acceso registrado correctamente',
                'record': {
                    'id': access_record.id,
                    'resident_name': permission.resident.get_full_name(),
                    'timestamp': access_record.timestamp.strftime('%d/%m/%Y %H:%M'),
                    'access_type': access_record.get_access_type_display(),
                    'permission_status': permission.status
                }
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
