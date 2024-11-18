from django.db import models

class CategorieArticle(models.Model):
    nom = models.CharField(max_length=100)
    taux_tva = models.DecimalField(max_digits=5, decimal_places=3, default=0)  # Check this field

    def __str__(self):
        return self.nom

