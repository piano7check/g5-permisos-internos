from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from .models import AccessRecord
from a_users.models import User
from a_permissions.models import Permission
import json
from django.db import models
from datetime import datetime, timedelta

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
        
        # Obtener fecha y hora actual
        now = timezone.now()
        today = now.date()
        today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
        today_end = timezone.make_aware(datetime.combine(today, datetime.max.time()))

        # Obtener los filtros seleccionados
        selected_statuses = self.request.GET.getlist('status')
        selected_areas = self.request.GET.getlist('area')
        date_filter = self.request.GET.get('date_filter', 'all')

        # Aplicar filtros de estado
        if selected_statuses:
            queryset = queryset.filter(status__in=selected_statuses)
        else:
            # Si no hay estados seleccionados, mostrar solo aprobados y vigentes
            queryset = queryset.filter(
                status='APPROVED',
                start_date__lte=now,
                end_date__gte=now
            )

        # Aplicar filtros de área
        if selected_areas:
            queryset = queryset.filter(resident__controlled_area__in=selected_areas)

        # Aplicar filtros de fecha
        if date_filter == 'today':
            # Permisos activos hoy (se cruzan con el día de hoy)
            queryset = queryset.filter(
                start_date__lte=today_end,
                end_date__gte=today_start
            )
        elif date_filter == 'tomorrow':
            # Calcular mañana
            tomorrow_start = today_start + timedelta(days=1)
            tomorrow_end = today_end + timedelta(days=1)
            
            # Permisos activos mañana
            queryset = queryset.filter(
                start_date__lte=tomorrow_end,
                end_date__gte=tomorrow_start
            )
        elif date_filter == 'week':
            # Calcular fin de semana (7 días desde hoy)
            week_end = today_end + timedelta(days=7)
            
            # Permisos que estarán activos en los próximos 7 días
            queryset = queryset.filter(
                start_date__lte=week_end,
                end_date__gte=today_start
            )

        # Ordenar por fecha de inicio
        return queryset.order_by('start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Opciones de filtros
        context['status_choices'] = Permission.STATUS_CHOICES
        context['area_choices'] = [
            ('MALE', 'Residencia Varones'),
            ('FEMALE', 'Residencia Mujeres')
        ]
        context['date_filter_choices'] = [
            ('today', 'Hoy'),
            ('tomorrow', 'Mañana'),
            ('week', 'Esta semana'),
            ('all', 'Todos')
        ]
        
        # Filtros seleccionados
        selected_statuses = self.request.GET.getlist('status')
        # Si no hay estados seleccionados, marcar APPROVED por defecto
        context['selected_statuses'] = selected_statuses if selected_statuses else ['APPROVED']
        context['selected_areas'] = self.request.GET.getlist('area')
        context['selected_date_filter'] = self.request.GET.get('date_filter', 'all')
        
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
        queryset = AccessRecord.objects.all().select_related(
            'resident', 
            'security_guard', 
            'permission'
        )

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

        # Filtro por área
        area = self.request.GET.get('area')
        if area in ['MALE', 'FEMALE']:
            queryset = queryset.filter(resident__controlled_area=area)

        return queryset.order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['residents'] = User.objects.filter(role='RESIDENTE')
        context['area_choices'] = [
            ('MALE', 'Residencia Varones'),
            ('FEMALE', 'Residencia Mujeres')
        ]
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

class PermissionDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'security/permission_detail.html'
    model = Permission
    context_object_name = 'permission'

    def test_func(self):
        return self.request.user.role == 'SEGURIDAD'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el último registro de acceso
        context['last_access'] = AccessRecord.objects.filter(
            permission=self.object
        ).order_by('-timestamp').first()
        return context
