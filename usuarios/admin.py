from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioPersonalizado

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'tipo_usuario', 'is_staff', 'is_superuser')
    list_filter = ('tipo_usuario', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name')}),
        ('Permisos', {'fields': ('tipo_usuario', 'is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'tipo_usuario', 'is_staff'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Staff no puede ver superusers
        if request.user.is_staff and not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Staff no puede asignar is_superuser
        if request.user.is_staff and not request.user.is_superuser:
            if 'is_superuser' in form.base_fields:
                form.base_fields['is_superuser'].disabled = True
        return form

    def has_delete_permission(self, request, obj=None):
        # Staff no puede eliminar superusers
        if request.user.is_staff and not request.user.is_superuser:
            if obj and obj.is_superuser:
                return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        # Staff no puede modificar superusers
        if request.user.is_staff and not request.user.is_superuser:
            if obj and obj.is_superuser:
                return False
        return super().has_change_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        # Staff no puede ver superusers
        if request.user.is_staff and not request.user.is_superuser:
            if obj and obj.is_superuser:
                return False
        return super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        # Staff puede crear usuarios, pero no superusers
        return super().has_add_permission(request)

admin.site.register(UsuarioPersonalizado, CustomUserAdmin)