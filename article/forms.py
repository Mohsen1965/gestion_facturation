from django import forms
from django_select2.forms import Select2Widget
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['code_article', 'nom', 'description', 'prix_unitaire', 'stock', 'categorie', 'tva']
        widgets = {
            'categorie': Select2Widget(attrs={'data-placeholder': 'Choisir une catégorie'}),
            'tva': Select2Widget(attrs={'data-placeholder': 'Choisir un taux TVA'}),
        }
