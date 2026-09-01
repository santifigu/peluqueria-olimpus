from django import forms
from datetime import date
from .models import Turno, Profesional, HorarioAtencion
from catalogo.models import Servicio


class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['servicio', 'profesional', 'nombre_cliente', 'email_cliente',
                  'telefono_cliente', 'fecha', 'hora', 'notas']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'notas': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicio'].queryset = Servicio.objects.filter(activo=True)
        self.fields['profesional'].queryset = Profesional.objects.filter(activo=True)
        self.fields['profesional'].required = False

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < date.today():
            raise forms.ValidationError("No podés reservar un turno en una fecha pasada.")
        return fecha

    def clean(self):
        cleaned = super().clean()
        profesional = cleaned.get('profesional')
        fecha = cleaned.get('fecha')
        hora = cleaned.get('hora')
        if profesional and fecha and hora:
            existe = Turno.objects.filter(
                profesional=profesional, fecha=fecha, hora=hora,
                estado__in=['pendiente', 'confirmado'],
            ).exists()
            if existe:
                raise forms.ValidationError("Ese horario ya está reservado con ese profesional. Elegí otro.")
        return cleaned
