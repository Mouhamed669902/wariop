from django import forms
from .models import Produit, Categorie
from django import forms
from .models import Commande

class AjouterProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        # On demande au vendeur de remplir la catégorie, le nom, la description, le prix et l'image.
        # Le champ 'vendeur' est masqué car on le liera automatiquement dans la vue !
        fields = ['categorie', 'nom', 'description', 'prix', 'image']

    # Validation simple pour s'assurer que le prix est logique
    def clean_prix(self):
        prix = self.cleaned_data.get('prix')
        if prix is not None and prix <= 0:
            raise forms.ValidationError("Le prix du produit doit être supérieur à 0 FCFA.")
        return prix

    class CommandeForm(forms.ModelForm):
        class Meta:
            model = Commande
            fields = ['nom_complet', 'telephone', 'adresse_livraison']
            widgets = {
                'nom_complet': forms.TextInput(
                    attrs={'class': 'w-full p-3 border rounded-lg', 'placeholder': 'Votre Nom complet'}),
                'telephone': forms.TextInput(
                    attrs={'class': 'w-full p-3 border rounded-lg', 'placeholder': 'Votre numéro de téléphone'}),
                'adresse_livraison': forms.Textarea(attrs={'class': 'w-full p-3 border rounded-lg', 'rows': 3,
                                                           'placeholder': 'Votre adresse de livraison'}),
            }