from django.contrib import admin
from .models import Categorie, Produit, Commande

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug']
    prepopulated_fields = {'slug': ('nom',)}

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ['nom', 'vendeur', 'prix', 'disponible', 'date_creation']
    list_filter = ['disponible', 'date_creation', 'vendeur']
    list_editable = ['prix', 'disponible']

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    # Remplace 'date_commande' par 'date_creation' si c'est le nom exact dans ton modèle
    list_display = ('id', 'nom_complet', 'telephone', 'total', 'date_creation')
    search_fields = ('nom_complet', 'telephone')