import cloudinary
import cloudinary.uploader

# Tes clés Cloudinary
cloudinary.config(
    cloud_name="dhtmc6vr1",
    api_key="479733683485777",
    api_secret="wpdsEZsJzmz0JgmScvxGglaB6G8"
)

print(f"Cloud name: {cloudinary.config().cloud_name}")
print(f"API Key: {cloudinary.config().api_key[:5]}...")
print("=" * 50)

# Test avec une image qui existe
try:
    print("📤 Test upload de GFQM2301.JPG...")
    result = cloudinary.uploader.upload("media/produits/GFQM2301.JPG", folder="test/")
    print("✅ Upload réussi !")
    print(f"URL: {result['secure_url']}")
except Exception as e:
    print(f"❌ Erreur: {e}")