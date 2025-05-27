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
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        
        # Si no es superusuario, hacer el campo role de solo lectura
        if not request.user.is_superuser:
            readonly_fields.append('role')
            readonly_fields.append('is_superuser')
            readonly_fields.append('is_staff')
            readonly_fields.append('groups')
            readonly_fields.append('user_permissions')
        
        return readonly_fields
    
    def has_change_permission(self, request, obj=None):
        # Solo permitir editar si es superusuario o si está editando su propio perfil
        if not obj:
            return True
        return request.user.is_superuser or request.user == obj
    
    def has_delete_permission(self, request, obj=None):
        # Solo permitir eliminar si es superusuario
        return request.user.is_superuser
