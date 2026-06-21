from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('boutique.urls')),    # Routes de la boutique à la racine (/)
    path('comptes/', include('comptes.urls')), # Routes d'authentification (/comptes/)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)