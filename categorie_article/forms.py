from django import forms
from .models import CategorieArticle

class CategorieArticleForm(forms.ModelForm):
    class Meta:
        model = CategorieArticle
        fields = ['nom', 'taux_tva']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'}),
            'taux_tva': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.001', 'placeholder': 'Taux TVA'}),
        }
        labels = {
            'nom': 'Nom de la catégorie',
            'taux_tva': 'Taux de TVA (%)',
        }


class CategorieArticleSearchForm(forms.Form):
    # Liste des champs que l'utilisateur peut choisir pour la recherche
    CHOICES_FIELDS = [
        ('nom', 'Nom de la catégorie'),
        ('taux_tva', 'Taux de TVA'),
    ]
    
    # Liste des opérateurs de comparaison
    CHOICES_OPERATORS = [
        ('exact', 'Exactement'),
        ('icontains', 'Contient'),
        ('gt', 'Supérieur à'),
        ('lt', 'Inférieur à'),
        ('gte', 'Supérieur ou égal à'),
        ('lte', 'Inférieur ou égal à'),
        ('range', 'Entre'),  # Ajout de l'opérateur "Entre"
    ]
    
    # Champ pour sélectionner le champ à rechercher
    field = forms.ChoiceField(choices=CHOICES_FIELDS, required=True, label="Champ à rechercher")
    
    # Champ pour choisir l'opérateur de comparaison
    operator = forms.ChoiceField(choices=CHOICES_OPERATORS, required=True, label="Opérateur")
    
    # Champ pour entrer la valeur de la recherche (utilisé pour tous les opérateurs sauf "Entre")
    value = forms.CharField(required=False, label="Valeur à rechercher")

    # Champs supplémentaires pour les recherches avec "Entre"
    range_min = forms.CharField(required=False, label="Borne inférieure")
    range_max = forms.CharField(required=False, label="Borne supérieure")

    def clean(self):
        """Validation des champs en fonction de l'opérateur choisi."""
        cleaned_data = super().clean()
        operator = cleaned_data.get('operator')
        value = cleaned_data.get('value')
        range_min = cleaned_data.get('range_min')
        range_max = cleaned_data.get('range_max')

        # Si l'opérateur est "range", vérifier que les deux bornes sont présentes
        if operator == 'range':
            if not range_min or not range_max:
                raise forms.ValidationError("Veuillez fournir une borne inférieure et une borne supérieure.")
        # Si l'opérateur n'est pas "range", vérifier que 'value' est présent
        elif not value:
            raise forms.ValidationError("Veuillez fournir une valeur pour la recherche.")

        return cleaned_data
