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

    def approuver_vendeurs(self, request, queryset):
        for vendeur in queryset:
            vendeur.est_approuve = True
            vendeur.save()

            # Tentative d'envoi d'email (si ça échoue, on continue)
            try:
                sujet = "✅ Votre boutique WARIOP est approuvée !"
                message = f"""
Bonjour {vendeur.user.username},

Félicitations ! Votre boutique "{vendeur.nom_boutique}" a été approuvée.

Rendez-vous sur WARIOP pour commencer à vendre :
👉 https://wariop.onrender.com

L'équipe WARIOP 🇨🇮
"""
                send_mail(
                    sujet,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [vendeur.user.email],
                    fail_silently=True,
                )
            except Exception as e:
                # L'email échoue mais on continue
                print(f"Email non envoyé à {vendeur.user.email}: {e}")
                pass

        self.message_user(request, f"✅ {queryset.count()} vendeur(s) approuvé(s).")

    approuver_vendeurs.short_description = "✅ Approuver les vendeurs sélectionnés"

    def desapprouver_vendeurs(self, request, queryset):
        for vendeur in queryset:
            vendeur.est_approuve = False
            vendeur.save()

        self.message_user(request, f"❌ {queryset.count()} vendeur(s) désapprouvé(s).")

    desapprouver_vendeurs.short_description = "❌ Désapprouver les vendeurs sélectionnés"

    def supprimer_vendeurs(self, request, queryset):
        for vendeur in queryset:
            email = vendeur.user.email
            username = vendeur.user.username

            try:
                sujet = "🗑️ Suppression de votre compte vendeur WARIOP"
                message = f"""
Bonjour {username},

Votre compte vendeur a été supprimé de WARIOP.

Si vous pensez qu'il s'agit d'une erreur, contactez l'administrateur.

L'équipe WARIOP 🇨🇮
"""
                send_mail(
                    sujet,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email non envoyé: {e}")
                pass

            vendeur.user.delete()

        self.message_user(request, f"🗑️ {queryset.count()} vendeur(s) supprimé(s).")

    supprimer_vendeurs.short_description = "🗑️ Supprimer les vendeurs sélectionnés"