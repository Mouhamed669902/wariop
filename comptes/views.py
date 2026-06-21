from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import InscriptionVendeurForm


def inscription_vendeur(request):
    if request.method == 'POST':
        form = InscriptionVendeurForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()

            # Créer le profil vendeur
            from .models import ProfilVendeur
            profil = ProfilVendeur.objects.create(
                user=user,
                nom_boutique=form.cleaned_data['nom_boutique'],
                telephone=form.cleaned_data['telephone'],
                adresse=form.cleaned_data['adresse'],
                est_approuve=False
            )

            # Email de confirmation d'inscription
            sujet = "📝 Demande d'inscription vendeur WARIOP"
            message = f"""
Bonjour {user.username},

Votre demande d'inscription en tant que vendeur sur WARIOP a bien été reçue.

Nous examinons votre dossier et nous vous tiendrons informé dès que votre boutique sera approuvée.

📋 Récapitulatif de votre demande :
- Nom de la boutique : {form.cleaned_data['nom_boutique']}
- Email : {user.email}
- Téléphone : {form.cleaned_data['telephone']}

Nous vous contacterons sous 24 à 48 heures.

L'équipe WARIOP 🇨🇮
"""
            try:
                send_mail(
                    sujet,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Erreur d'envoi d'email: {e}")

            return render(request, 'comptes/succes.html', {
                'nom_boutique': form.cleaned_data['nom_boutique'],
                'email': user.email
            })
        else:
            messages.error(request, "❌ Veuillez corriger les erreurs ci-dessous.")
    else:
        form = InscriptionVendeurForm()

    return render(request, 'comptes/inscription_vendeur.html', {'form': form})


def deconnexion(request):
    logout(request)
    return redirect('/')