from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ProfilVendeur


class InscriptionVendeurForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse email", widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 border border-stone-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500',
        'placeholder': 'exemple@email.com'
    }))
    nom_boutique = forms.CharField(max_length=200, required=True, label="Nom de la boutique",
                                   widget=forms.TextInput(attrs={
                                       'class': 'w-full px-4 py-2 border border-stone-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500',
                                       'placeholder': 'Ma super boutique'
                                   }))
    telephone = forms.CharField(max_length=20, required=True, label="Numéro de téléphone",
                                widget=forms.TextInput(attrs={
                                    'class': 'w-full px-4 py-2 border border-stone-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500',
                                    'placeholder': '07 00 00 00 00'
                                }))
    adresse = forms.CharField(label="Adresse physique", widget=forms.Textarea(attrs={
        'class': 'w-full px-4 py-2 border border-stone-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500',
        'rows': 3,
        'placeholder': 'Votre adresse complète...'
    }), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Supprimer tous les messages d'aide
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['username'].help_text = ""  # ← Supprime le message
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-stone-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500',
            'placeholder': 'Choisissez un nom d\'utilisateur'
        })

        self.fields['email'].help_text = ""  # ← Supprime le message

        self.fields['password1'].label = "Mot de passe"
        self.fields['password1'].help_text = ""  # ← Supprime les messages de validation
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-stone-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500',
            'placeholder': 'Choisissez un mot de passe'
        })

        self.fields['password2'].label = "Confirmation du mot de passe"
        self.fields['password2'].help_text = ""  # ← Supprime le message
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-stone-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500',
            'placeholder': 'Confirmez votre mot de passe'
        })