from django import forms
from django.forms import modelformset_factory
from .models import Devis, LigneDevis  # Remplacez Facture et LigneFacture par Devis et LigneDevis


class DevisForm(forms.ModelForm):
    class Meta:
        model = Devis
        fields = ['numero_devis', 'date_devis', 'client', 'total_ht', 'total_tva', 'total_ttc']
        widgets = {
            'numero_devis': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
            }),
            'client': forms.Select(attrs={
                'class': 'form-control',
                'onchange': 'this.classList.remove("placeholder")'
            }),
            'date_devis': forms.DateInput(attrs={
                'type': 'date',
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            # Générer le numéro de devis uniquement pour les nouveaux devis
            last_devis = Devis.objects.all().order_by('id').last()
            last_num = int(last_devis.numero_devis.split('-')[-1]) if last_devis else 0
            next_num = last_num + 1  # Incrémentation du dernier numéro

            # Génération du numéro de devis avec un format comme DV-XXXX
            self.fields['numero_devis'].initial = f"DVS-{next_num:04d}"

        self.fields['client'].empty_label = "Sélectionner le Client"

    def save(self, commit=True):
        # Assurer que numero_devis est bien défini avant l'enregistrement
        if not self.instance.pk and not self.instance.numero_devis:
            self.instance.numero_devis = self.fields['numero_devis'].initial
        return super().save(commit=commit)


class LigneDevisForm(forms.ModelForm):
    quantite = forms.IntegerField(required=False, initial=0)  # Valeur initiale pour éviter les erreurs
    prix_unitaire = forms.DecimalField(required=False, initial=0.000)
    taux_remise = forms.DecimalField(required=False, initial=0.000)

    class Meta:
        model = LigneDevis
        fields = ['article', 'quantite', 'prix_unitaire', 'taux_remise']
        widgets = {
           'article': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; height: 24px;',

            }),  # Ajustez la largeur ici

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['article'].empty_label = "Sélectionner l'article"
        self.fields['taux_remise'].initial = 0.000  # S'assure que la remise est initialisée à 0.00
        self.fields['prix_unitaire'].widget.attrs.update({'class': 'form-control'})


# Formset pour gérer les lignes de devis
LigneDevisFormSet = modelformset_factory(
    LigneDevis,
    form=LigneDevisForm,
    extra=1,  # Nombre de formulaires supplémentaires affichés
)


class DevisSearchForm(forms.Form):
    # Liste des champs que l'utilisateur peut choisir pour la recherche
    CHOICES_FIELDS = [
        ('numero_devis', 'Numéro du devis'),
        ('client__nom', 'Nom du client'),  # Assuming 'Devis' has a foreign key to 'Client' with a 'nom' field
        ('date_devis', 'Date du devis'),
        ('total_ht', 'Total HT'),
        ('total_ttc', 'Total TTC'),
        ('etat', 'État du devis'),  # Assuming 'Devis' has a status field like 'etat'
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
