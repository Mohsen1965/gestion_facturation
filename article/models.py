from django.db import models
from categorie_article.models import CategorieArticle
from tva.models import TVA

class Article(models.Model):
    code_article = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)  # Allow this field to be optional
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=3)
    stock = models.IntegerField(blank=True, null=True)  # Allow this field to be optional
    categorie = models.ForeignKey(CategorieArticle, on_delete=models.CASCADE)
    tva = models.ForeignKey(TVA, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

