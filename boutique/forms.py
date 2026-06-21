from django import forms
from .models import Produit, Categorie

class AjouterProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['categorie', 'nom', 'description', 'prix', 'image', 'disponible']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }