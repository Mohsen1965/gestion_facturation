from django.db import models

class TVA(models.Model):
    taux_tva = models.DecimalField(max_digits=5, decimal_places=3)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.taux_tva}%"
