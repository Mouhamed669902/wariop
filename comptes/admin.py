from django.contrib import admin
from .models import ProfilVendeur


@admin.register(ProfilVendeur)
class ProfilVendeurAdmin(admin.ModelAdmin):
    # 'user__email' permet d'aller chercher l'email depuis le modèle User lié
    list_display = ('nom_boutique', 'user', 'user_email', 'telephone', 'est_approuve', 'date_demande')
    list_filter = ('est_approuve',)
    search_fields = ('nom_boutique', 'user__username', 'user__email')

    # Cette méthode permet de créer une colonne virtuelle "Email" dans l'admin
    def user_email(self, obj):
        return obj.user.email

    # Nom de l'en-tête de la colonne dans l'admin
    user_email.short_description = 'Email'