from django.db import models
from facture.models import Facture
from tva.models import TVA

class TVA_Facture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    taux_tva = models.ForeignKey(TVA, on_delete=models.CASCADE)
    montant_total_tva = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f"TVA {self.taux_tva.taux}% - Facture {self.facture.id}"
