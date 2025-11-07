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

🚀 Guía de Instalación y Ejecución
Sigue estos pasos para poner en marcha el proyecto en tu máquina local.

1. Clonar el Repositorio
Bash

git clone https://github.com/agustiinwilliamsoninacap/taller-de-dise-o-y-soluciones-.git
2. Navegar a la Carpeta del Proyecto
Bash

cd taller-de-dise-o-y-soluciones-/mermeladas_django_con_produccion
3. Crear y Activar un Entorno Virtual
Es una buena práctica aislar las dependencias de tu proyecto.

Bash

# Crear el entorno virtual
python -m venv venv

# Activar en Windows
.\venv\Scripts\activate

# Activar en macOS/Linux
source venv/bin/activate
4. Instalar Dependencias
Nota Importante: Sería ideal crear un archivo requirements.txt en tu proyecto (con pip freeze > requirements.txt) y subirlo al repositorio. De esta forma, otros solo necesitarían ejecutar pip install -r requirements.txt.

Como no hay un requirements.txt, instalaremos Django manualmente:

Bash

pip install django
(Si usas otras librerías como reportlab, instálalas aquí también: pip install reportlab)

5. Configurar la Base de Datos
Aplica las migraciones para crear las tablas en la base de datos (esto creará un archivo db.sqlite3).

Bash

python manage.py migrate
6. Crear un Superusuario
Necesitarás un usuario administrador para acceder al panel de Django.

Bash

python manage.py createsuperuser
(Te pedirá un nombre de usuario, email y contraseña)

7. Ejecutar el Servidor
¡Todo listo! Inicia el servidor de desarrollo.

Bash

python manage.py runserver
8. Acceder a la Aplicación
Abre tu navegador web y visita las siguientes URLs:

Sitio Principal: http://127.0.0.1:8000/

Panel de Admin: http://127.0.0.1:8000/admin (Usa los datos del superusuario)

## 📂 Estructura del Proyecto

Una vista simplificada de la estructura de carpetas del proyecto Django:

```text
mermeladas_django_con_produccion/
├── manage.py                   # Script principal de gestión de Django
├── [NOMBRE_PROYECTO_CONFIG]/   # Carpeta de configuración (settings.py, urls.py)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── [NOMBRE_APP_MERMELADAS]/    # Tu aplicación principal (models, views)
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── urls.py (opcional)
│   ├── templates/                # Aquí van tus archivos HTML
│   └── static/                   # Aquí van tus archivos CSS/JS/Imágenes
└── db.sqlite3                    # Tu base de datos
📄 Licencia
Este proyecto no tiene una licencia definida.

```

(Recomendación: "Este proyecto está bajo la Licencia MIT".)

🧑‍💻 Autores
Agustín Williamson

Fernanda Jara

Javiera Elgueta

GitHub: @agustiinwilliamsoninacap







## 🚀 Características Principales
CRUD Completo: Gestión total (Crear, Leer, Actualizar, Borrar) para Productos, Clientes y Materias Primas.

Sistema de Recetas: Permite crear recetas complejas que asocian un producto final con una lista de materias primas (ingredientes) usando formsets de Django.

Módulo de Producción: Una vista dedicada para "fabricar" productos a partir de recetas. Esta acción descuenta automáticamente el stock de materias primas y añade stock al producto final en un lote específico.

Punto de Venta (POS): Una interfaz de "Crear Venta" que valida el stock en tiempo real y calcula totales y cambios.

Gestión de Inventario FEFO: El sistema descuenta el stock del producto vendido utilizando la lógica FEFO (First Expired, First Out), asegurando que los lotes más próximos a vencer se vendan primero.

Generación de Comprobantes en PDF: Genera un PDF con el detalle de cada venta utilizando ReportLab.

Protección de Datos: Evita que se eliminen registros (Productos, Clientes, Materias Primas) si están asociados a otras operaciones (ventas, recetas), manejando el error ProtectedError.

## 📋 Módulos y Lógica de Vistas (Detalle de views.py)
A continuación se detalla la lógica implementada en el archivo views.py de la aplicación.

## 🏠 Home
home: Vista principal que actúa como un dashboard. Muestra estadísticas rápidas como el número total de productos, clientes y ventas.

## 📦 Productos
 ProductListView: Lista todos los productos registrados.
 
 ProductCreateView / ProductUpdateView: Vistas basadas en clases (CBV) para crear y editar productos.
 
 ProductDeleteView: CBV para eliminar un producto. Lógica clave: Intercepta ProtectedError para evitar el borrado si el producto está vinculado a ventas o recetas.

## 🙋‍♂️ Clientes
ClientListView: Lista todos los clientes.

ClientCreateView / ClientUpdateView: CBVs para crear y editar clientes.

ClientDeleteView: CBV para eliminar un cliente. Lógica clave: Evita el borrado si el cliente tiene ventas asociadas.

cliente_detalle: Vista de detalle que muestra la información del cliente, su total histórico gastado y una lista detallada de todas sus compras.

## 🌾 Materias Primas
RawMaterialListView: Lista todas las materias primas (ingredientes).

RawMaterialCreateView / RawMaterialUpdateView: CBVs para crear y editar materias primas.

RawMaterialDeleteView: CBV para eliminar una materia prima. Lógica clave: Evita el borrado si la materia prima se está utilizando en alguna receta.

## 🍳 Recetas y Producción
RecipeListView / receta_detalle: Vistas para listar y ver el detalle de una receta (producto final e ingredientes).

receta_crear / receta_editar: Vistas complejas que utilizan un RecipeForm (para la receta) y un RecipeItemFormSet (para los ingredientes) en la misma página. Ambas operaciones se envuelven en transaction.atomic para garantizar la integridad de los datos.

receta_producir: Lógica de negocio fundamental para la fabricación.

Recibe la cantidad a producir (multiplicador) y los datos del lote.

Valida Stock: Comprueba si hay suficientes materias primas para la producción solicitada.

Descuenta Stock (Materias Primas): Si la validación es exitosa, resta las cantidades de RawMaterial.stock.

Crea Lote (Producto Final): Crea un nuevo ProductBatch (Lote de Producto) con la cantidad fabricada y sus fechas de producción/vencimiento.

Actualiza Stock Total: Recalcula el Product.stock del producto final sumando todos sus lotes activos.

## 🛒 Ventas (POS y FEFO)
SaleListView / venta_detalle: Vistas para el historial y detalle de ventas.

venta_crear: El "Punto de Venta" principal.

Utiliza un SaleForm (para el cliente/pago) y un SaleItemFormSet (para los productos).

Validación de Stock: Comprueba que la cantidad total solicitada de cada producto no supere el Product.stock disponible.

Validación de Pago: Si es "EFECTIVO", valida que el monto pagado sea suficiente.

Lógica FEFO: Llama a la función _descontar_por_FEFO por cada producto vendido.

_descontar_por_FEFO (Helper): Esta función implementa la lógica FEFO.

Obtiene todos los lotes (ProductBatch) del producto, ordenados por fecha de vencimiento.

Resta la cantidad vendida del lote más próximo a vencer.

Si el lote se agota, continúa descontando del siguiente lote, y así sucesivamente.

Finalmente, actualiza el Product.stock general.

venta_pdf: Utiliza ReportLab para generar un comprobante de venta en formato PDF, listo para imprimir o descargar.

## 🛠️ Tecnologías Utilizadas
Backend: Django

Generación de PDF: ReportLab

Base de Datos: (PostgreSQL,Render)








