# Mermeladas (Django con Producción y FEFO)

## Requisitos
- Python 3.10+
- pip, venv
- (Opcional) PyCharm

## Pasos
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Features
- Productos (CLP enteros), Clientes, Ventas (PDF), Materias Primas
- Recetas con ingredientes
- **Producción desde recetas**: descuenta materias primas, crea Lote (FEFO) y aumenta stock del producto final
- **FEFO en ventas**: descuenta stock desde lotes con vencimiento más próximo
- Historial de compras por cliente + PDF individual
