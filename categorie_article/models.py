from django.db import models
from django.utils.timezone import now

class CategorieArticle(models.Model):
    nom = models.CharField(max_length=100)
    taux_tva = models.DecimalField(max_digits=5, decimal_places=3, default=0)  # Check this field
    created_at = models.DateTimeField(default=now, editable=False)  # Ajout du champ created_at

    def __str__(self):
        return self.nom
