from django import forms
from .models import Resena


class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['puntaje', 'comentario']
        widgets = {
            'puntaje': forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(1, 6)]),
            'comentario': forms.Textarea(attrs={'rows': 3}),
        }
