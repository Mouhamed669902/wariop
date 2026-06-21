import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wariop_project.settings')
django.setup()

from boutique.models import Produit

print("🔍 Nettoyage des URLs d'images...")
print("=" * 50)

for produit in Produit.objects.all():
    if produit.image:
        ancien = str(produit.image)
        print(f"Produit: {produit.nom}")
        print(f"Avant: {ancien}")

        # Si l'image contient une URL Cloudinary complète
        if ancien.startswith('https://res.cloudinary.com/'):
            # Extraire la partie après /upload/
            if '/upload/' in ancien:
                # Garder seulement ce qui est après le dernier /upload/
                parts = ancien.split('/upload/')
                if len(parts) > 1:
                    # Prendre la dernière partie (après le dernier /upload/)
                    nouveau = parts[-1]
                    produit.image = nouveau
                    produit.save()
                    print(f"Après: {nouveau}")
                    print("✅ Nettoyé")
                else:
                    print("⏭️ Format non reconnu")
            else:
                print("⏭️ Pas de /upload/ trouvé")
        else:
            # Vérifier si l'image commence par 'produits/'
            if ancien.startswith('produits/'):
                print(f"⏭️ Déjà au bon format")
            else:
                # Ajouter 'produits/' devant
                nouveau = f"produits/{ancien}"
                produit.image = nouveau
                produit.save()
                print(f"Après: {nouveau}")
                print("✅ Ajout de produits/")

        print("-" * 30)
    else:
        print(f"Produit: {produit.nom} - Pas d'image")
        print("-" * 30)

print("✅ Nettoyage terminé !")