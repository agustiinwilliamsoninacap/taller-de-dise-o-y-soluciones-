from pathlib import Path
import os

# Rutas base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta
SECRET_KEY = 'django-insecure-change-this-in-production'

# Configuración de depuración (False en producción)
DEBUG = False

ALLOWED_HOSTS = [
    "taller-de-dise-o-y-soluciones-1.onrender.com",  # exacto
    ".onrender.com",                                  # subdominios de Render
    "localhost",
    "127.0.0.1",
]
CSRF_TRUSTED_ORIGINS = [
    "https://taller-de-dise-o-y-soluciones-1.onrender.com",
    "https://*.onrender.com",

]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mermeladas_django.ventas',  # ruta completa de tu app
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URLs y WSGI (usando rutas completas)
ROOT_URLCONF = 'mermeladas_django.mermeladas.urls'
WSGI_APPLICATION = 'mermeladas_django.mermeladas.wsgi.application'

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de contraseñas (puedes agregar los predeterminados si deseas)
AUTH_PASSWORD_VALIDATORS = []

# Configuración regional
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # importante para Render

# Tipo de campo automático
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "ERROR"},
}
