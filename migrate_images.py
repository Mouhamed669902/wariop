import os
import django
from cloudinary.uploader import upload
import cloudinary

# 🔥 CONFIGURATION FORCEE
cloudinary.config(
    cloud_name="dhtmc6vr1",
    api_key="479733683485777",
    api_secret="wpdsEZsJzmz0JgmScvxGglaB6G8"
)

# 🔥 FORCER LES VARIABLES D'ENVIRONNEMENT
os.environ['CLOUDINARY_CLOUD_NAME'] = "dhtmc6vr1"
os.environ['CLOUDINARY_API_KEY'] = "479733683485777"
os.environ['CLOUDINARY_API_SECRET'] = "wpdsEZsJzmz0JgmScvxGglaB6G8"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wariop_project.settings')
django.setup()

from boutique.models import Produit

print("🚀 Migration des images vers Cloudinary...")
print("=" * 50)
print(f"Cloud name: {os.environ.get('CLOUDINARY_CLOUD_NAME')}")
print(f"API Key: {os.environ.get('CLOUDINARY_API_KEY')[:5]}...")
print("=" * 50)

compteur = 0
total = Produit.objects.count()

for produit in Produit.objects.all():
    if produit.image and not produit.image.url.startswith('http'):
        try:
            print(f"📤 Upload de {produit.nom}...")
            result = upload(produit.image.path, folder='produits/')
            produit.image = result['secure_url']
            produit.save()
            compteur += 1
            print(f"✅ [{compteur}/{total}] {produit.nom} migré")
        except Exception as e:
            print(f"❌ Erreur pour {produit.nom}: {e}")
    else:
        print(f"⏭️ {produit.nom} déjà sur Cloudinary ou sans image")

print("=" * 50)
print(f"✅ Migration terminée ! {compteur} image(s) migrée(s)")