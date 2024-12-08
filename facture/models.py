from django.db import models
from client.models import Client
from article.models import Article
from django.utils import timezone
from tva.models import TVA
from decimal import Decimal
from decimal import InvalidOperation
from django.utils.timezone import now


class Facture(models.Model):
    numero_facture = models.CharField(max_length=100)
    date_facture = models.DateField(default=timezone.now)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    total_ht = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    total_tva = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    total_ttc = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    STATUTS = [
        ('impayee', 'Impayée'),  # Option 1
        ('payee', 'Payée'),      # Option 2
    ]
    etat = models.CharField(max_length=20, choices=STATUTS, default='impayée')
    created_at = models.DateTimeField(default=now, editable=False)  # Ajout du champ

    def __str__(self):
        return f"Facture {self.numero_facture} - {self.client}"


class LigneFacture(models.Model):
    facture = models.ForeignKey(Facture, related_name='lignes_facture', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    taux_remise = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    montant_ht = models.DecimalField(max_digits=10, decimal_places=3, editable=False)
    montant_remise = models.DecimalField(max_digits=10, decimal_places=3, default=0, editable=False)
    montant_tva = models.DecimalField(max_digits=10, decimal_places=3, editable=False)
    montant_ttc = models.DecimalField(max_digits=10, decimal_places=3, editable=False)

    def save(self, *args, **kwargs):
        # Convert quantite and prix_unitaire to Decimal, handling conversion errors
        try:
            quantite = Decimal(self.quantite) if self.quantite is not None else Decimal('0.000')
            prix_unitaire = Decimal(self.prix_unitaire) if self.prix_unitaire is not None else Decimal('0.000')
        except (ValueError, InvalidOperation) as e:
            print(f"Error converting quantite or prix_unitaire to Decimal: {e}")
            quantite = Decimal('0.000')
            prix_unitaire = Decimal('0.000')

        # Ensure taux_remise is set to 0 if not provided
        self.taux_remise = self.taux_remise or Decimal('0.000')

        # Calculating Montant HT with Remise included
        self.montant_ht = (quantite * prix_unitaire) * (1 - (self.taux_remise / Decimal(100)))
        
        # Calculating Montant Remise for reference
        self.montant_remise = self.montant_ht * (self.taux_remise / Decimal(100))

        # Calculate Montant TVA if TVA is provided
        tva = self.article.tva
        if tva:
            print(f"Article: {self.article.nom}, TVA Rate: {tva.taux_tva}")
            self.montant_tva = self.montant_ht * (Decimal(tva.taux_tva) / Decimal(100))
        else:
            print(f"No TVA found for article: {self.article.nom}")
            self.montant_tva = Decimal(0)

        # Calculate Montant TTC
        self.montant_ttc = self.montant_ht + self.montant_tva

        # Save the instance
        super().save(*args, **kwargs)