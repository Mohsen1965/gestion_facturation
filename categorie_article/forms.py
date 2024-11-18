from django import forms
from .models import CategorieArticle

class CategorieArticleForm(forms.ModelForm):
    class Meta:
        model = CategorieArticle
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'})
        }
