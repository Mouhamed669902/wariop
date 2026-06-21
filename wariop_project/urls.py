from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('boutique.urls')),
    path('comptes/', include('comptes.urls')),
]

# 🔥 CORRECTION : Sert les fichiers media même en production
# Si tu utilises Cloudinary, commente ces lignes
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # En production, Django ne sert pas les fichiers media
    # Utilise Cloudinary ou Render Disk
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)