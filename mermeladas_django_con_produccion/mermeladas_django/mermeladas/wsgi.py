import os
from django.core.wsgi import get_wsgi_application

# módulo de settings del proyecto
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "mermeladas_django.mermeladas.settings",
)

application = get_wsgi_application()
