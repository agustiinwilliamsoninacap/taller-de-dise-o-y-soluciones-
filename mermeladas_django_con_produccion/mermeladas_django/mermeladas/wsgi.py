import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Asegura que Python vea la carpeta raíz del proyecto (donde está 'ventas')
BASE_DIR = Path(__file__).resolve().parents[2]  # .../mermeladas_django_con_produccion
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "mermeladas_django.mermeladas.settings"
)

application = get_wsgi_application()
