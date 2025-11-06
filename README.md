# 🚀 Proyecto: Taller de Diseño y Soluciones (Mermeladas Django)

Este repositorio alberga el proyecto final para la asignatura "Taller de Diseño y Soluciones". El proyecto principal, ubicado en la carpeta `mermeladas_django_con_produccion`, es una aplicación web desarrollada con Python y el framework Django.

## 📝 Descripción del Proyecto

*(Esta es la sección más importante. Reemplaza este texto con tu descripción.)*

**Ejemplo:**
"Esta aplicación web sirve como un sistema para la gestión de producción y venta de mermeladas artesanales. Permite a los administradores registrar nuevos productos (sabores), gestionar el inventario disponible, y procesar pedidos de clientes. El objetivo es centralizar la operación del negocio en una plataforma digital."

---

## ✨ Características Principales

*(Lista las cosas que tu aplicación puede hacer. Aquí hay algunos ejemplos genéricos para un proyecto de mermeladas, ¡ajústalos a tu proyecto!)*

* **Gestión de Productos:** CRUD (Crear, Leer, Actualizar, Borrar) completo para los tipos de mermeladas.
* **Control de Inventario:** Sistema para monitorear las cantidades (stock) de cada producto.
* **Autenticación de Usuarios:** Sistema de Login y Registro para clientes y administradores.
* **Panel de Administración:** Uso del panel de Django Admin (`/admin`) para una gestión de datos sencilla.
* **Catálogo Público:** Vista pública donde los visitantes pueden ver los productos disponibles.

---

## 💻 Pila Tecnológica (Tech Stack)

* **Backend:** Python 3, Django
* **Base de Datos:** SQLite3 (por defecto en desarrollo)
* **Frontend:** HTML5, CSS3 *(Añade JavaScript/Bootstrap si los usaste)*

---

## ⚙️ Guía de Instalación y Ejecución Local

Sigue estos pasos para levantar el proyecto en tu máquina local.

### 1. Prerrequisitos

* Tener [Python 3.10+](https://www.python.org/downloads/) instalado.
* Tener [Git](https://git-scm.com/) instalado.

### 2. Clonar el Repositorio

```bash
git clone [https://github.com/agustiinwilliamsoninacap/taller-de-dise-o-y-soluciones-.git](https://github.com/agustiinwilliamsoninacap/taller-de-dise-o-y-soluciones-.git)
cd taller-de-dise-o-y-soluciones-
3. Navegar a la Carpeta del Proyecto
Todo el código de Django está dentro de la carpeta mermeladas_django_con_produccion.

Bash

cd mermeladas_django_con_produccion
4. Crear y Activar un Entorno Virtual
Es una buena práctica aislar las dependencias de tu proyecto.

Bash

# Crear el entorno virtual
python -m venv venv

# Activar en Windows
.\venv\Scripts\activate

# Activar en macOS/Linux
source venv/bin/activate
5. Instalar Dependencias
(Importante: Sería ideal que crearas un archivo requirements.txt en tu proyecto con el comando pip freeze > requirements.txt y lo subieras al repositorio. Así, otros solo tendrían que ejecutar pip install -r requirements.txt.)

Como no hay un requirements.txt, instalaremos Django manualmente:

Bash

pip install django
6. Configurar la Base de Datos
Aplica las migraciones para crear las tablas en la base de datos (creará un archivo db.sqlite3).

Bash

python manage.py migrate
7. Crear un Superusuario
Necesitarás un usuario administrador para acceder a http://127.0.0.1:8000/admin.

Bash

python manage.py createsuperuser
(Te pedirá un nombre de usuario, email y contraseña)

8. Ejecutar el Servidor
¡Todo listo! Inicia el servidor de desarrollo.

Bash

python manage.py runserver
9. Acceder a la Aplicación
Abre tu navegador web y visita las siguientes URLs:

Sitio Principal: http://127.0.0.1:8000/

Panel de Admin: http://127.0.0.1:8000/admin (Usa los datos del superusuario que creaste)

📂 Estructura del Proyecto
(Reemplaza [NOMBRE_PROYECTO_CONFIG] y [NOMBRE_APP_MERMELADAS] con los nombres reales de tus carpetas)

Una vista simplificada de la estructura de carpetas del proyecto Django:

mermeladas_django_con_produccion/
├── manage.py               # Script principal de gestión de Django
├── [NOMBRE_PROYECTO_CONFIG]/ # Carpeta de configuración (settings.py, urls.py)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── [NOMBRE_APP_MERMELADAS]/  # Tu aplicación principal (models, views)
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── urls.py (opcional)
│   ├── templates/          # Aquí van tus archivos HTML
│   └── static/             # Aquí van tus archivos CSS/JS/Imágenes
└── db.sqlite3              # Tu base de datos
📄 Licencia
Este proyecto no tiene una licencia definida.

(Si quieres, puedes añadir una licencia MIT. Es la más común y permisiva. Simplemente reemplaza la línea de arriba con: "Este proyecto está bajo la Licencia MIT".)

🧑‍💻 Autor
Agustín Williamson , Fernanda Jara, Javiera Elgueta 

GitHub: @agustiinwilliamsoninacap
