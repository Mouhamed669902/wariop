from django.apps import AppConfig

class ComptesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comptes'

    def ready(self):
        # Cette ligne magique importe et active tes signaux au lancement du serveur
        import comptes.signals