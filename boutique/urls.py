from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_produits, name='liste_produits'),
    path('vendeur/ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('panier/', views.voir_panier, name='voir_panier'),
    path('panier/ajouter/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/vider/', views.vider_panier, name='vider_panier'),
    path('panier/modifier/<int:produit_id>/', views.modifier_quantite, name='modifier_quantite'),
    path('commande/valider/', views.valider_commande, name='valider_commande'),
    path('panier/supprimer/<int:produit_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('admin-dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('commande/statut/<int:commande_id>/<str:nouveau_statut>/', views.changer_statut_commande, name='changer_statut'),
]