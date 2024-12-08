from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['code_client', 'nom', 'adresse', 'email', 'telephone', 'ville', 'compte', 'matricule_fiscal']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom du client'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email du client'}),
            'telephone': forms.TextInput(attrs={'placeholder': 'Téléphone du client'}),
            'adresse': forms.TextInput(attrs={'placeholder': 'Adresse du client'}),
            'ville': forms.TextInput(attrs={'placeholder': 'Ville'}),
            'compte': forms.TextInput(attrs={'placeholder': 'Compte'}),
            'matricule_fiscal': forms.TextInput(attrs={'placeholder': 'Matricule fiscal'}),
        }


class ClientSearchForm(forms.Form):
    # Liste des champs que l'utilisateur peut choisir pour la recherche
    CHOICES_FIELDS = [
        ('code_client', 'Code Client'),
        ('nom', 'Nom'),
        ('ville', 'Ville'),
        ('compte', 'Compte'),
        ('telephone', 'Téléphone'),
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
