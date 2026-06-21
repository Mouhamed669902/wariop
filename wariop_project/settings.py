from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-g50bw+5@5l2x--0^skb7!icov3&p1w$$y1ba@ee-a+8e@e*fvc'
DEBUG = False

ALLOWED_HOSTS = ['wariop.onrender.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'boutique',
    'comptes',
    # 👇 AJOUTE CLOUDINARY (si tu veux l'utiliser)
    # 'cloudinary',
    # 'cloudinary_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Déjà présent
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wariop_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wariop_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- FICHIERS STATIQUES ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 🔥 CORRECTION ICI : Le bon chemin pour ton dossier static
STATICFILES_DIRS = [
    BASE_DIR / 'boutique' / 'static',  # ✅ Corrigé
]

# --- FICHIERS MÉDIA ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- OPTION 1 : Utiliser Cloudinary (RECOMMANDÉ) ---
# Décommente si tu veux utiliser Cloudinary
# import cloudinary
# cloudinary.config(
#     cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
#     api_key=os.environ.get('CLOUDINARY_API_KEY'),
#     api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
# )
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# --- OPTION 2 : Stockage local (avec Render Disk) ---
# DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'omouhamadou69@gmail.com'
EMAIL_HOST_PASSWORD = 'lqbwblsbzardsxgi'
DEFAULT_FROM_EMAIL = f"WARIOP E-commerce <{EMAIL_HOST_USER}>"
SUPERADMIN_EMAIL = 'omouhamadou69@gmail.com'