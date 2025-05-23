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

# Create your views here.

class RegisterAccessView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'security/register_access.html'

    def test_func(self):
        return self.request.user.role == 'SEGURIDAD'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener residentes del área controlada por el guardia
        context['residents'] = User.objects.filter(
            role='RESIDENTE',
            controlled_area=self.request.user.controlled_area
        )
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
            resident_id = data.get('resident_id')
            access_type = data.get('access_type')
            notes = data.get('notes', '')

            if not resident_id or not access_type:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Faltan datos requeridos'
                }, status=400)

            resident = get_object_or_404(
                User,
                id=resident_id,
                role='RESIDENTE',
                controlled_area=request.user.controlled_area
            )

            # Verificar si hay un permiso activo para entradas
            active_permission = None
            if access_type == 'ENTRY':
                active_permission = Permission.objects.filter(
                    resident=resident,
                    status='APPROVED',
                    start_date__lte=timezone.now(),
                    end_date__gte=timezone.now()
                ).first()

                if not active_permission:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'El residente no tiene un permiso activo para entrar'
                    }, status=400)

            # Crear el registro de acceso
            access_record = AccessRecord.objects.create(
                resident=resident,
                security_guard=request.user,
                access_type=access_type,
                notes=notes,
                permission=active_permission
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Acceso registrado correctamente',
                'record': {
                    'id': access_record.id,
                    'resident_name': resident.get_full_name(),
                    'timestamp': access_record.timestamp.strftime('%d/%m/%Y %H:%M'),
                    'access_type': access_record.get_access_type_display()
                }
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
