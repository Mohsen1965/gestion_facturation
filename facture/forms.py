from django import forms
from django.forms import modelformset_factory
from .models import Facture, LigneFacture


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
                'class': 'form-control',
                'onchange': 'this.classList.remove("placeholder")'
            }),
            'date_facture': forms.DateInput(attrs={
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
            'etat': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                'style': 'height: 25px; width: 100%;',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['article'].empty_label = "Sélectionner l'article"
        self.fields['taux_remise'].initial = 0.000  # S'assure que la remise est initialisée à 0.00


# Formset pour gérer les lignes de facture
LigneFactureFormSet = modelformset_factory(
    LigneFacture,
    form=LigneFactureForm,
    extra=1,  # Nombre de formulaires supplémentaires affichés
)