from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import ProfilVendeur


@receiver(pre_save, sender=ProfilVendeur)
def notifier_decision_vendeur(sender, instance, **kwargs):
    # Si le profil existe déjà dans la base (c'est une modification dans l'admin)
    if instance.pk:
        try:
            # Récupérer l'état du profil avant que ta modification ne soit enregistrée
            ancien_profil = ProfilVendeur.objects.get(pk=instance.pk)

            # --- SCÉNARIO A : APPROBATION (Passage de décoché à coché) ---
            if not ancien_profil.est_approuve and instance.est_approuve:
                sujet = "🎉 Félicitations ! Votre boutique WARIOP a été approuvée"
                message = (
                    f"Bonjour {instance.user.username},\n\n"
                    f"Bonne nouvelle ! Après vérification par notre équipe, votre compte vendeur pour la boutique "
                    f"'{instance.nom_boutique}' a été validé avec succès.\n\n"
                    f"Vous pouvez dès à présent vous connecter sur WARIOP et ajouter vos produits en ligne !\n\n"
                    f"Cordialement,\nL'équipe WARIOP."
                )
                send_mail(
                    sujet,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [instance.user.email],
                    fail_silently=False
                )

            # --- SCÉNARIO B : REFUS / SUSPENSION (Passage de coché à décoché) ---
            elif ancien_profil.est_approuve and not instance.est_approuve:
                sujet = "⚠️ Mise à jour concernant votre compte vendeur WARIOP"
                message = (
                    f"Bonjour {instance.user.username},\n\n"
                    f"Nous vous informons qu'après réévaluation, le statut de votre boutique '{instance.nom_boutique}' "
                    f"a été modifié et votre accès vendeur a été refusé ou suspendu.\n\n"
                    f"Si vous pensez qu'il s'agit d'une erreur ou si vous souhaitez soumettre de nouveaux éléments, "
                    f"veuillez contacter le support WARIOP.\n\n"
                    f"Cordialement,\nL'équipe WARIOP."
                )
                send_mail(
                    sujet,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [instance.user.email],
                    fail_silently=False
                )

        except ProfilVendeur.DoesNotExist:
            pass