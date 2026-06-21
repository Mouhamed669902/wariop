from django.db import models
from django.contrib.auth.models import User

class ProfilVendeur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profilvendeur')
    nom_boutique = models.CharField(max_length=200, default="Ma boutique")
    telephone = models.CharField(max_length=20, default="00000000")
    adresse = models.TextField(default="Adresse à renseigner")
    est_approuve = models.BooleanField(default=False)
    date_demande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom_boutique} - {self.user.username}"