from django.db import models

class Client(models.Model):
    code_client = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True) 
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.nom
