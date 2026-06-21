from django.db import models
from django.contrib.auth.models import User
from comptes.models import ProfilVendeur  # On importe le modèle vendeur


class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nom


class Produit(models.Model):
    # Lie le produit à un vendeur. Si le vendeur est supprimé, ses produits aussi.
    vendeur = models.ForeignKey(ProfilVendeur, on_delete=models.CASCADE, related_name='produits', null=True, blank=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produits')
    nom = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)  # En FCFA par exemple
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


# ICI : La classe Commande est maintenant bien en dehors de Produit !
class Commande(models.Model):
    # Informations de livraison du client
    nom_complet = models.CharField(max_length=200, verbose_name="Nom complet")
    telephone = models.CharField(max_length=20, verbose_name="Numéro de téléphone")
    adresse_livraison = models.TextField(verbose_name="Adresse complète de livraison")
    date_creation = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0.0)

    # Un texte récapitulatif simple pour lister les produits achetés dans l'admin
    resume_produits = models.TextField(verbose_name="Articles commandés", blank=True)
    # AJOUTE CE BLOC ICI, JUSTE SOUS LES CHAMPS EXISTANTS
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours de livraison'),
        ('livre', 'Livré'),
    ]

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )

    # ... fin de tes champs ...

    def __str__(self):
        return f"Commande #{self.id} - {self.nom_complet} ({self.total} FCFA)"