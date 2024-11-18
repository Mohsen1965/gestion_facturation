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
                'style': 'height: 25px; width: 100%;',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['article'].empty_label = "Sélectionner l'article"
        self.fields['taux_remise'].initial = 0.000  # S'assure que la remise est initialisée à 0.00


# Formset pour gérer les lignes de devis
LigneDevisFormSet = modelformset_factory(
    LigneDevis,
    form=LigneDevisForm,
    extra=1,  # Nombre de formulaires supplémentaires affichés
)
