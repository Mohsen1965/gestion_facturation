from django import forms
from django.forms import modelformset_factory
from .models import Facture, LigneFacture, Article


class FactureForm(forms.ModelForm):
    ETAT_CHOICES = [
        ('payé', 'Payé'),
        ('impayé', 'Impayé'),
    ]

    class Meta:
        model = Facture
        fields = ['numero_facture', 'date_facture', 'client', 'total_ht', 'total_tva', 'total_ttc', 'etat']
        widgets = {
            'numero_facture': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
            }),
            'client': forms.Select(attrs={
                'class': 'form-control select2',
                'onchange': 'this.classList.remove("placeholder")'
            }),
            'date_facture': forms.DateInput(attrs={
                'type': 'date',  # HTML5 date picker
                'class': 'form-control',
            }),
        
            'total_ht': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
            }),
            'total_tva': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
            }),
            'total_ttc': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
            }),
            'etat': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convertir la date au format ISO pour le champ HTML si elle existe
        if self.instance and self.instance.date_facture:
            self.fields['date_facture'].initial = self.instance.date_facture.strftime('%Y-%m-%d')


        if not self.instance.pk:
            # Générer le numéro de la facture uniquement pour les nouvelles factures
            last_facture = Facture.objects.all().order_by('id').last()
            last_num = int(last_facture.numero_facture.split('-')[-1]) if last_facture else 0
            next_num = last_num + 1  # Incrémentation du dernier numéro

            # Génération du numéro de facture avec un format comme FCT-XXXX
            self.fields['numero_facture'].initial = f"FCT-{next_num:04d}"

        self.fields['client'].empty_label = "Sélectionner le Client"
        self.fields['etat'].initial = 'impayé'  # Valeur par défaut pour l'état

    def save(self, commit=True):
        # Assurer que numero_facture est bien défini avant l'enregistrement
        if not self.instance.pk and not self.instance.numero_facture:
            self.instance.numero_facture = self.fields['numero_facture'].initial
        return super().save(commit=commit)


class LigneFactureForm(forms.ModelForm):
    quantite = forms.IntegerField(required=False, initial=0)  # Valeur initiale pour éviter les erreurs
    prix_unitaire = forms.DecimalField(required=False, initial=0.000)
    taux_remise = forms.DecimalField(required=False, initial=0.000)

    class Meta:
        model = LigneFacture
        fields = ['article', 'quantite', 'prix_unitaire', 'taux_remise']
        widgets = {
            'article': forms.Select(attrs={
                'class': 'select_article',  # Ajouter un ID unique pour le champ article
                'style': 'width: 100%; height: 25px;',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['article'].empty_label = "Sélectionner l'article"
        self.fields['taux_remise'].initial = 0.000  # S'assure que la remise est initialisée à 0.00
        self.fields['prix_unitaire'].widget.attrs.update({'readonly': 'readonly'})



# Formset pour gérer les lignes de facture
LigneFactureFormSet = modelformset_factory(
    LigneFacture,
    form=LigneFactureForm,
    extra=1,  # Nombre de formulaires supplémentaires affichés
)


class FactureSearchForm(forms.Form):
    # Liste des champs que l'utilisateur peut choisir pour la recherche
    CHOICES_FIELDS = [
        ('numero_facture', 'Numéro de la facture'),
        ('client', 'Client'),
        ('date_facture', 'Date de la facture'),
        ('total_ht', 'Total HT'),
        ('total_ttc', 'Total TTC'),
        ('compte', 'Compte'),

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
