from django import forms
from django.utils import timezone
from .models import Permission

class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['reason', 'start_date', 'end_date']
        widgets = {
            'reason': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Describe el motivo de tu solicitud de permiso'
            }),
            'start_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'required': True
                }
            ),
            'end_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'required': True
                }
            ),
        }
        error_messages = {
            'reason': {
                'required': 'Por favor, ingresa el motivo de tu solicitud.'
            },
            'start_date': {
                'required': 'Por favor, selecciona la fecha y hora de inicio.'
            },
            'end_date': {
                'required': 'Por favor, selecciona la fecha y hora de fin.'
            }
        }

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date:
            now = timezone.now()
            if start_date < now:
                raise forms.ValidationError('La fecha de inicio debe ser posterior a la fecha actual.')
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        
        if end_date and start_date:
            if end_date <= start_date:
                raise forms.ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')
        return end_date

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        reason = cleaned_data.get('reason')

        if reason and len(reason.strip()) < 10:
            self.add_error('reason', 'El motivo debe tener al menos 10 caracteres.')

        if start_date and end_date:
            # Verificar que el permiso no sea por más de 7 días
            duration = end_date - start_date
            if duration.days > 7:
                self.add_error('end_date', 'El permiso no puede ser por más de 7 días.')

        return cleaned_data 

# elimiar estos campos 

# fields = ['resident', 'approver', 'destination', 'reason', 'start_date', 'end_date']