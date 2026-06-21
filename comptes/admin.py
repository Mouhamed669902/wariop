from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import ProfilVendeur


@admin.register(ProfilVendeur)
class ProfilVendeurAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'email', 'nom_boutique', 'telephone', 'est_approuve', 'date_demande']
    list_filter = ['est_approuve']
    search_fields = ['nom_boutique', 'user__username', 'user__email', 'telephone']
    list_editable = ['est_approuve']
    actions = ['approuver_vendeurs', 'desapprouver_vendeurs', 'supprimer_vendeurs']

    def email(self, obj):
        return obj.user.email

    email.short_description = "Email"

    # ✅ Action : Approuver les vendeurs
    def approuver_vendeurs(self, request, queryset):
        for vendeur in queryset:
            vendeur.est_approuve = True
            vendeur.save()

            # Email de confirmation d'approbation
            sujet = "✅ Votre boutique WARIOP est approuvée !"
            message = f"""
Bonjour {vendeur.user.username},

Félicitations ! Votre boutique "{vendeur.nom_boutique}" a été approuvée par l'administrateur de WARIOP.

Vous pouvez maintenant :
- Ajouter vos produits en ligne
- Gérer votre boutique
- Vendre en toute confiance

Rendez-vous sur WARIOP pour commencer à vendre :
👉 https://wariop.onrender.com

Merci de faire partie de la communauté WARIOP 🇨🇮

L'équipe WARIOP
"""
            try:
                send_mail(
                    sujet,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [vendeur.user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Erreur d'envoi d'email: {e}")

        self.message_user(request, f"✅ {queryset.count()} vendeur(s) approuvé(s) et email(s) envoyé(s).")

    approuver_vendeurs.short_description = "✅ Approuver les vendeurs sélectionnés"

    # ❌ Action : Désapprouver les vendeurs
    def desapprouver_vendeurs(self, request, queryset):
        for vendeur in queryset:
            vendeur.est_approuve = False
            vendeur.save()

            # Email de désapprobation
            sujet = "❌ Votre boutique WARIOP n'a pas été approuvée"
            message = f"""
Bonjour {vendeur.user.username},

Nous vous informons que votre boutique "{vendeur.nom_boutique}" n'a pas été approuvée pour le moment.

Pour plus d'informations, veuillez contacter l'administrateur.

L'équipe WARIOP 🇨🇮
"""
            try:
                send_mail(
                    sujet,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [vendeur.user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Erreur d'envoi d'email: {e}")

        self.message_user(request, f"❌ {queryset.count()} vendeur(s) désapprouvé(s) et email(s) envoyé(s).")

    desapprouver_vendeurs.short_description = "❌ Désapprouver les vendeurs sélectionnés"

    # 🗑️ Action : Supprimer les vendeurs (avec email)
    def supprimer_vendeurs(self, request, queryset):
        for vendeur in queryset:
            email = vendeur.user.email
            username = vendeur.user.username
            nom_boutique = vendeur.nom_boutique

            # Email avant suppression
            sujet = "🗑️ Suppression de votre compte vendeur WARIOP"
            message = f"""
Bonjour {username},

Nous vous informons que votre compte vendeur "{nom_boutique}" a été supprimé de la plateforme WARIOP.

Si vous pensez qu'il s'agit d'une erreur, veuillez contacter l'administrateur.

L'équipe WARIOP 🇨🇮
"""
            try:
                send_mail(
                    sujet,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Erreur d'envoi d'email: {e}")

            # Supprimer l'utilisateur (le profil sera supprimé automatiquement à cause de OneToOne)
            vendeur.user.delete()

        self.message_user(request, f"🗑️ {queryset.count()} vendeur(s) supprimé(s) et email(s) envoyé(s).")

    supprimer_vendeurs.short_description = "🗑️ Supprimer les vendeurs sélectionnés"