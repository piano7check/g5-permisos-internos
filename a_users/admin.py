from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'gender', 'controlled_area', 'is_active')
    list_filter = ('role', 'gender', 'controlled_area', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información Personal'), {'fields': ('first_name', 'last_name', 'phone', 'gender')}),
        (_('Permisos y Roles'), {
            'fields': ('role', 'controlled_area', 'is_active', 'is_staff', 'is_superuser'),
            'classes': ('wide',),
            'description': _('Configura los roles y permisos del usuario. El superusuario tiene acceso completo.')
        }),
        (_('Grupos y Permisos Específicos'), {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',),
            'description': _('Los grupos proporcionan una manera de aplicar permisos a múltiples usuarios.')
        }),
        (_('Fechas Importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'first_name', 'last_name'),
        }),
    )
    
    readonly_fields = ('last_login', 'date_joined')
    filter_horizontal = ('groups', 'user_permissions')
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        # Solo los superusuarios no tienen campos readonly
        if not request.user.is_superuser:
            readonly_fields += ['is_superuser', 'is_staff']
        return readonly_fields

    def has_change_permission(self, request, obj=None):
        # Permitir a staff editar cualquier usuario excepto superusuarios
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # Permitir a staff eliminar cualquier usuario excepto superusuarios
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return True
