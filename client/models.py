from django.db import models

class Client(models.Model):
    code_client = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, unique=True) 
    telephone = models.CharField(max_length=20, blank=True)  # Non obligatoire
    ville = models.CharField(max_length=20, blank=True)      # Non obligatoire
    compte = models.CharField(max_length=20, blank=True)     # Non obligatoire
    matricule_fiscal = models.CharField(max_length=20, blank=True)  # Non obligatoire
    created_at = models.DateTimeField(auto_now_add=True)       # Champ qui enregistre automatiquement la date de création

    def __str__(self):
        return self.nom
