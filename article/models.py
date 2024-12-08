from django.db import models
from categorie_article.models import CategorieArticle
from tva.models import TVA

class Article(models.Model):
    code_article = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)  
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=3)
    stock = models.IntegerField(blank=True, null=True)
    categorie = models.ForeignKey(CategorieArticle, on_delete=models.CASCADE)
    tva = models.ForeignKey(TVA, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically adds the timestamp

    def __str__(self):
        return self.nom
