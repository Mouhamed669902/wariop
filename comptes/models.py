from django.db import models
from django.contrib.auth.models import User


class ProfilVendeur(models.Model):
    # On lie ce profil à un utilisateur de base Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_vendeur')
    nom_boutique = models.CharField(max_length=150)
    telephone = models.CharField(max_length=20)
    description_activite = models.TextField(blank=True)

    # Le statut de validation par TOI (le boss)
    est_approuve = models.BooleanField(default=False)
    date_demande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Boutique : {self.nom_boutique} ({self.user.username})"