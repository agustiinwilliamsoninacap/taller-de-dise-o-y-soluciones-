from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-change-this-in-production"
DEBUG = False

ALLOWED_HOSTS = [
    ".onrender.com",                               # todos los subdominios de Render
        "taller-de-dise-o-y-soluciones-1.onrender.com",   # tu URL actual
            "taller-de-dise-o-y-soluciones--1.onrender.com",  # por si tu servicio usa doble guion
                "localhost", "127.0.0.1",
                ]

                CSRF_TRUSTED_ORIGINS = [
                    "https://taller-de-dise-o-y-soluciones-1.onrender.com",
                        "https://taller-de-dise-o-y-soluciones--1.onrender.com",
                            "https://*.onrender.com",
                            ]

                            SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

                            INSTALLED_APPS = [
                                "whitenoise.runserver_nostatic",   # antes que staticfiles (mejor DX)
                                    "django.contrib.admin",
                                        "django.contrib.auth",
                                            "django.contrib.contenttypes",
                                                "django.contrib.sessions",
                                                    "django.contrib.messages",
                                                        "django.contrib.staticfiles",
                                                            "mermeladas_django.ventas",
                                                            ]

                                                            MIDDLEWARE = [
                                                                "django.middleware.security.SecurityMiddleware",
                                                                    "whitenoise.middleware.WhiteNoiseMiddleware",  # servir estáticos en Render
                                                                        "django.contrib.sessions.middleware.SessionMiddleware",
                                                                            "django.middleware.common.CommonMiddleware",
                                                                                "django.middleware.csrf.CsrfViewMiddleware",
                                                                                    "django.contrib.auth.middleware.AuthenticationMiddleware",
                                                                                        "django.contrib.messages.middleware.MessageMiddleware",
                                                                                            "django.middleware.clickjacking.XFrameOptionsMiddleware",
                                                                                            ]

                                                                                            ROOT_URLCONF = "mermeladas_django.mermeladas.urls"
                                                                                            WSGI_APPLICATION = "mermeladas_django.mermeladas.wsgi.application"

                                                                                            TEMPLATES = [
                                                                                                {
                                                                                                        "BACKEND": "django.template.backends.django.DjangoTemplates",
                                                                                                                "DIRS": [BASE_DIR / "templates"],  # si tienes carpeta templates global
                                                                                                                        "APP_DIRS": True,
                                                                                                                                "OPTIONS": {
                                                                                                                                            "context_processors": [
                                                                                                                                                            "django.template.context_processors.debug",
                                                                                                                                                                            "django.template.context_processors.request",
                                                                                                                                                                                            "django.contrib.auth.context_processors.auth",
                                                                                                                                                                                                            "django.contrib.messages.context_processors.messages",
                                                                                                                                                                                                                        ],
                                                                                                                                                                                                                                },
                                                                                                                                                                                                                                    },
                                                                                                                                                                                                                                    ]

                                                                                                                                                                                                                                    DATABASES = {
                                                                                                                                                                                                                                        "default": {
                                                                                                                                                                                                                                                "ENGINE": "django.db.backends.sqlite3",
                                                                                                                                                                                                                                                        "NAME": BASE_DIR / "db.sqlite3",
                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                            }

                                                                                                                                                                                                                                                            AUTH_PASSWORD_VALIDATORS = []  # agrega validadores si los necesitas

                                                                                                                                                                                                                                                            LANGUAGE_CODE = "es-cl"
                                                                                                                                                                                                                                                            TIME_ZONE = "America/Santiago"
                                                                                                                                                                                                                                                            USE_I18N = True
                                                                                                                                                                                                                                                            USE_TZ = True

                                                                                                                                                                                                                                                            # Archivos estáticos
                                                                                                                                                                                                                                                            STATIC_URL = "static/"
                                                                                                                                                                                                                                                            STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
                                                                                                                                                                                                                                                            STATIC_ROOT = BASE_DIR / "staticfiles"   # collectstatic

                                                                                                                                                                                                                                                            # WhiteNoise: comprimir y añadir manifiesto (mejores headers)
                                                                                                                                                                                                                                                            STORAGES = {
                                                                                                                                                                                                                                                                "staticfiles": {
                                                                                                                                                                                                                                                                        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
                                                                                                                                                                                                                                                                            },
                                                                                                                                                                                                                                                                            }

                                                                                                                                                                                                                                                                            DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

                                                                                                                                                                                                                                                                            # log a consola (para ver tracebacks reales en Render)
                                                                                                                                                                                                                                                                            LOGGING = {
                                                                                                                                                                                                                                                                                "version": 1,
                                                                                                                                                                                                                                                                                    "disable_existing_loggers": False,
                                                                                                                                                                                                                                                                                        "handlers": {"console": {"class": "logging.StreamHandler"}},
                                                                                                                                                                                                                                                                                            "root": {"handlers": ["console"], "level": "ERROR"},
                                                                                                                                                                                                                                                                                            }
                                                                                                                                                                                                                                                                                            