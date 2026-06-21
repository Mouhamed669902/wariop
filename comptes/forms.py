from django import forms
from django.contrib.auth.models import User
from .models import ProfilVendeur

class InscriptionVendeurForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe")
    email = forms.EmailField(label="Adresse Email")

    class Meta:
        model = ProfilVendeur
        fields = ['nom_boutique', 'telephone', 'description_activite']

    # --- SÉCURITÉ ET MESSAGE SIMPLE ICI ---
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # On vérifie dans la base de données si ce nom existe déjà
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.")
        return username

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        profil = super().save(commit=False)
        profil.user = user
        if commit:
            profil.save()
        return profil