from django import forms
from .models import TVA

class TVAForm(forms.ModelForm):
    class Meta:
        model = TVA
        fields = ['taux_tva', 'description']
        widgets = {
            'taux_tva': forms.NumberInput(attrs={'step': '0.01'}),
            'description': forms.TextInput(attrs={'placeholder': 'Enter a description'}),
        }
