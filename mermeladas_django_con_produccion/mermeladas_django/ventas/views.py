# --- Importaciones ---
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages  # Para mostrar notificaciones al usuario
from django.views.generic import ListView, CreateView, UpdateView, DeleteView  # Vistas Basadas en Clases (CRUD)
from django.db import transaction  # Para asegurar que operaciones complejas (ej. Venta) sean "atómicas"
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4  # Para el PDF
from reportlab.pdfgen import canvas  # Para dibujar el PDF
from reportlab.lib.units import cm  # Para usar centímetros en el PDF
from django.db.models.deletion import ProtectedError  # Para capturar errores al borrar (ej. un cliente con ventas)
import json

# Importar modelos y formularios de la app actual
from .models import Product, Client, RawMaterial, Recipe, RecipeItem, Sale, SaleItem, ProductBatch
from .forms import ProductForm, ClientForm, RawMaterialForm, RecipeForm, RecipeItemFormSet, SaleForm, SaleItemFormSet, \
    ProductionForm

# --- Vistas Principales ---

def home(request):
    """
    Vista principal (Dashboard) que muestra contadores básicos.
    """
    datos = {
        "total_productos": Product.objects.count(),
        "total_clientes": Client.objects.count(),
        "total_ventas": Sale.objects.count(),
    }
    return render(request, "home.html", datos)


# --- Sección: Productos ---
# Se usan Vistas Basadas en Clases (CBV) para un CRUD estándar.

class ProductListView(ListView):
    """ Muestra una lista de todos los productos. """
    model = Product
    template_name = "productos/list.html"
    context_object_name = "productos"


class ProductCreateView(CreateView):
    """ Muestra un formulario para crear un nuevo producto. """
    model = Product
    form_class = ProductForm
    template_name = "productos/form.html"
    success_url = reverse_lazy("productos_list")  # Redirige a la lista al éxito


class ProductUpdateView(UpdateView):
    """ Muestra un formulario para editar un producto existente. """
    model = Product
    form_class = ProductForm
    template_name = "productos/form.html"
    success_url = reverse_lazy("productos_list")


class ProductDeleteView(DeleteView):
    """ Pide confirmación y elimina un producto. """
    model = Product
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("productos_list")

    # --- BUENA PRÁCTICA: Añadir protección contra borrado ---
    def post(self, request, *args, **kwargs):
        """
        Sobrescribe el método POST para capturar ProtectedError.
        Esto evita borrar un producto que esté siendo usado en ventas o recetas.
        """
        self.object = self.get_object()
        try:
            # Intenta eliminar el objeto como lo haría normalmente
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            # Si falla porque está protegido (ej. por una ForeignKey on_delete=PROTECT)
            sales_count = self.object.saleitem_set.count()  # Cuántas ventas lo usan
            recipes_count = self.object.recipe_set.count() # Cuántas recetas lo usan
            messages.error(request,
                           f"No se puede eliminar '{self.object.nombre}', está en {sales_count} ventas y {recipes_count} recetas.")
            return redirect(self.success_url)


# --- Sección: Clientes ---

class ClientListView(ListView):
    """ Muestra una lista de todos los clientes. """
    model = Client
    template_name = "clientes/list.html"
    context_object_name = "clientes"


class ClientCreateView(CreateView):
    """ Muestra un formulario para crear un nuevo cliente. """
    model = Client
    form_class = ClientForm
    template_name = "clientes/form.html"
    success_url = reverse_lazy("clientes_list")


class ClientUpdateView(UpdateView):
    """ Muestra un formulario para editar un cliente existente. """
    model = Client
    form_class = ClientForm
    template_name = "clientes/form.html"
    success_url = reverse_lazy("clientes_list")


class ClientDeleteView(DeleteView):
    """ Pide confirmación y elimina un cliente. """
    model = Client
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("clientes_list")

    def post(self, request, *args, **kwargs):
        """
        Protección contra borrado: No permite borrar un cliente si tiene ventas asociadas.
        """
        self.object = self.get_object()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            sales_count = self.object.sale_set.count()
            messages.error(request,
                           f"No se puede eliminar '{self.object.nombre}' porque tiene {sales_count} venta(s) asociada(s).")
            return redirect(self.success_url)


def cliente_detalle(request, pk):
    """
    Vista de detalle personalizada para un cliente.
    Muestra info del cliente, su total gastado y su historial de ventas.
    """
    cliente = get_object_or_404(Client, pk=pk)
    
    # Importar Sum para cálculos de agregación
    from django.db.models import Sum
    
    # Calcula el total gastado por este cliente sumando el campo 'total' de todas sus ventas
    cliente.total_gastado = Sale.objects.filter(cliente=cliente).aggregate(total=Sum('total'))['total'] or 0

    # Obtiene las ventas de este cliente
    ventas = Sale.objects.filter(cliente=cliente).prefetch_related("items", "items__producto")
    return render(request, "clientes/detail.html", {"cliente": cliente, "ventas": ventas})


# --- Sección: Materias Primas ---

class RawMaterialListView(ListView):
    """ Muestra una lista de todas las materias primas. """
    model = RawMaterial
    template_name = "materias/list.html"
    context_object_name = "materias"


class RawMaterialCreateView(CreateView):
    """ Muestra un formulario para crear una nueva materia prima. """
    model = RawMaterial
    form_class = RawMaterialForm
    template_name = "materias/form.html"
    success_url = reverse_lazy("materias_list")


class RawMaterialUpdateView(UpdateView):
    """ Muestra un formulario para editar una materia prima existente. """
    model = RawMaterial
    form_class = RawMaterialForm
    template_name = "materias/form.html"
    success_url = reverse_lazy("materias_list")


class RawMaterialDeleteView(DeleteView):
    """ Pide confirmación y elimina una materia prima. """
    model = RawMaterial
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("materias_list")

    def post(self, request, *args, **kwargs):
        """
        Protección contra borrado: No permite borrar una materia prima si se usa en recetas.
        """
        self.object = self.get_object()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            # Encuentra todos los ítems de receta que usan esta materia prima
            recetas = self.object.recipeitem_set.select_related("receta")
            # Crea una lista única de nombres de recetas
            nombres = ", ".join(sorted({ri.receta.nombre for ri in recetas}))
            messages.error(request, f"No se puede eliminar '{self.object.nombre}' porque se usa en recetas: {nombres}.")
            return redirect(self.success_url)


# --- Sección: Recetas ---
# Se usan Vistas Basadas en Funciones (FBV) porque manejan Formsets (receta + ingredientes)

class RecipeListView(ListView):
    """ Muestra una lista de todas las recetas. """
    model = Recipe
    template_name = "recetas/list.html"
    context_object_name = "recetas"


def receta_crear(request):
    """
    Vista para crear una Receta y sus RecipeItems (ingredientes) usando un Formset.
    """
    receta = Recipe()
    # Pasa un mapa de unidades (ej. {1: "Kg", 2: "Lt"}) al JS del frontend
    unidades = {m.pk: m.unidad for m in RawMaterial.objects.all()}

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=receta)
        formset = RecipeItemFormSet(request.POST, instance=receta)

        if form.is_valid() and formset.is_valid():
            # Usar 'transaction.atomic' para asegurar que o se guarda TODO (receta e ítems) o NADA
            with transaction.atomic():
                receta = form.save()
                formset.instance = receta  # Asigna la receta recién creada al formset
                formset.save()  # Guarda los ítems del formset
            messages.success(request, "Receta creada correctamente.")
            return redirect("recetas_list")
    else:
        # Petición GET: Muestra formularios vacíos
        form = RecipeForm(instance=receta)
        formset = RecipeItemFormSet(instance=receta)

    return render(request, "recetas/form.html", {
        "form": form,
        "formset": formset,
        "unidades": json.dumps(unidades)  # Convertir a JSON para JS
    })


def receta_editar(request, pk):
    """
    Vista para editar una Receta y sus RecipeItems (ingredientes) usando un Formset.
    """
    receta = get_object_or_404(Recipe, pk=pk)
    unidades = {m.pk: m.unidad for m in RawMaterial.objects.all()}

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=receta)
        formset = RecipeItemFormSet(request.POST, instance=receta)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, "Receta actualizada correctamente.")
            return redirect("recetas_list")
    else:
        # Petición GET: Muestra formularios con datos existentes
        form = RecipeForm(instance=receta)
        formset = RecipeItemFormSet(instance=receta)

    return render(request, "recetas/form.html", {
        "form": form,
        "formset": formset,
        "unidades": json.dumps(unidades)
    })


def receta_detalle(request, pk):
    """ Muestra el detalle de una receta y sus ingredientes. """
    receta = get_object_or_404(Recipe, pk=pk)
    return render(request, "recetas/detail.html", {"receta": receta})


@transaction.atomic  # Decorador para asegurar que la producción es todo o nada
def receta_producir(request, pk):
    """
    Vista para "producir" una receta.
    Esto resta stock de materias primas y añade stock al producto final (lote).
    """
    receta = get_object_or_404(Recipe, pk=pk)
    if not receta.producto_final:
        messages.error(request, "Esta receta no tiene producto final asignado.")
        return redirect("receta_detail", pk=pk)

    if request.method == "POST":
        form = ProductionForm(request.POST)
        if form.is_valid():
            # Obtener datos del formulario de producción
            mult = form.cleaned_data["multiplicador"]
            cod = form.cleaned_data["codigo_lote"]
            fprod = form.cleaned_data["fecha_produccion"]
            fven = form.cleaned_data["fecha_vencimiento"]

            # 1. Verificar stock de materias primas
            faltantes = []
            for item in receta.items.select_related("materia_prima"):
                req = item.cantidad * mult  # Cantidad requerida de materia prima
                if item.materia_prima.stock < req:
                    faltantes.append(
                        f"{item.materia_prima.nombre} (requiere {req}, disponible {item.materia_prima.stock})")
            
            if faltantes:
                # Si falta stock, mostrar error y no hacer nada
                messages.error(request, "Stock insuficiente: " + "; ".join(faltantes))
                return redirect("receta_detail", pk=pk)

            # 2. Descontar stock de materias primas (si hay suficiente)
            for item in receta.items.select_related("materia_prima"):
                req = item.cantidad * mult
                mp = item.materia_prima
                mp.stock = mp.stock - req
                mp.save()

            # 3. Crear el Lote (ProductBatch) del producto final
            unidades = receta.rendimiento_unidades * mult  # Unidades producidas
            ProductBatch.objects.create(
                producto=receta.producto_final,
                codigo_lote=cod,
                fecha_produccion=fprod,
                fecha_vencimiento=fven,
                cantidad=unidades
            )
            
            # 4. Actualizar el stock total del producto final
            producto = receta.producto_final
            # El stock total es la suma de todos sus lotes activos
            producto.stock = sum(lote.cantidad for lote in producto.lotes.filter(cantidad__gt=0))
            producto.save()

            messages.success(request, f"Producción registrada: +{unidades} {producto.unidad} al lote {cod}.")
            return redirect("receta_detail", pk=pk)
    else:
        form = ProductionForm()
    return render(request, "recetas/produccion_form.html", {"form": form, "receta": receta})


# --- Helper de FEFO (First Expiring, First Out) ---

def _descontar_por_FEFO(producto, cantidad):
    """
    Función auxiliar para descontar stock siguiendo la lógica FEFO.
    Descuenta 'cantidad' del 'producto', empezando por los lotes que vencen antes.
    """
    restante = float(cantidad)
    # 1. Obtener lotes con stock, ordenados por vencimiento (y luego producción/id como desempate)
    lotes = list(producto.lotes.filter(cantidad__gt=0).order_by("fecha_vencimiento", "fecha_produccion", "id"))

    # 2. Verificación de seguridad: ¿Hay suficiente stock en lotes?
    stock_en_lotes = sum(l.cantidad for l in lotes)
    if stock_en_lotes < restante:
        # Si el stock total del producto está desactualizado, corregirlo
        producto.stock = stock_en_lotes
        producto.save()
        return False  # No hay suficiente stock

    # 3. Descontar de los lotes
    for lote in lotes:
        if restante <= 0:
            break
        disp = float(lote.cantidad)  # Disponible en este lote
        tomar = min(disp, restante)  # Cuánto tomar de este lote
        lote.cantidad = disp - tomar
        lote.save()
        restante -= tomar  # Actualizar lo que falta por descontar

    # 4. Recalcular el stock total del producto (suma de lotes restantes)
    producto.stock = sum(l.cantidad for l in producto.lotes.filter(cantidad__gt=0))
    producto.save()
    
    # Devuelve True si se pudo descontar todo (o casi todo, por errores de precisión)
    return restante <= 0.0001


# --- Sección: Ventas ---

class SaleListView(ListView):
    """ Muestra una lista del historial de ventas. """
    model = Sale
    template_name = "ventas/list.html"
    context_object_name = "ventas"


@transaction.atomic  # La creación de venta DEBE ser atómica
def venta_crear(request):
    """
    Vista para crear una nueva Venta.
    Implica validar stock, guardar la venta, guardar ítems y descontar stock por FEFO.
    """
    venta = Sale()
    # Optimización: Obtener solo productos activos y con stock
    productos = Product.objects.filter(activo=True, stock__gt=0)
    # Crear mapas de precios y stock para pasar al JS del frontend
    precios = {p.id: int(p.precio_unitario) for p in productos}
    stock_map = {p.id: float(p.stock) for p in productos}

    if request.method == "POST":
        form = SaleForm(request.POST, instance=venta)
        formset = SaleItemFormSet(request.POST, instance=venta)

        if form.is_valid() and formset.is_valid():
            total_provisional = 0
            productos_a_descontar = {}  # Para agrupar (ej. si venden 2kg y 1kg del mismo producto)

            # --- 1. PRIMERA PASADA: Validar ítems y calcular total provisional ---
            for f in formset.forms:
                if not f.cleaned_data or f.cleaned_data.get("DELETE"):
                    continue  # Ignorar formularios vacíos o marcados para borrar
                
                producto = f.cleaned_data.get("producto")
                cantidad = f.cleaned_data.get("cantidad")
                
                # Validar que la fila no esté a medio llenar
                if not producto or not cantidad:
                    messages.error(request, "Se detectó una fila de producto vacía. Por favor, complétela o márquela para eliminar.")
                    return render(request, "ventas/form.html", {"form": form, "formset": formset, "precios": precios, "stock_map": json.dumps(stock_map)})

                # Agrupar cantidades por producto
                productos_a_descontar[producto] = productos_a_descontar.get(producto, 0) + cantidad
                # Calcular total
                precio = f.cleaned_data.get("precio_unitario") or int(producto.precio_unitario)
                total_provisional += int(precio) * float(cantidad)

            # --- ARREGLO PARA EVITAR VENTAS EN $0 ---
            if not productos_a_descontar:
                messages.error(request, "No se puede registrar una venta sin productos.")
                return render(request, "ventas/form.html", {"form": form, "formset": formset, "precios": precios, "stock_map": json.dumps(stock_map)})

            # --- 2. SEGUNDA PASADA: Validar stock total ---
            for producto, cantidad_total in productos_a_descontar.items():
                if cantidad_total > producto.stock:
                    messages.error(request, f"Stock insuficiente para {producto.nombre}. Se solicitan {cantidad_total} y hay {producto.stock} disponible(s).")
                    return render(request, "ventas/form.html", {"form": form, "formset": formset, "precios": precios, "stock_map": json.dumps(stock_map)})

            # --- 3. VALIDAR PAGO (si es efectivo) ---
            metodo = form.cleaned_data.get("metodo_pago")
            pagado = form.cleaned_data.get("monto_pagado") or 0
            if metodo == "EFECTIVO" and int(pagado) < int(total_provisional):
                messages.error(request, f"Monto pagado insuficiente. Total: ${int(total_provisional)} CLP.")
                return render(request, "ventas/form.html", {"form": form, "formset": formset, "precios": precios, "stock_map": json.dumps(stock_map)})

            # --- 4. GUARDAR VENTA (Maestro) ---
            venta = form.save(commit=False)
            venta.total = int(total_provisional)
            venta.cambio = int(pagado) - int(venta.total) if metodo == "EFECTIVO" else 0
            venta.save()  # Guardar la venta para obtener un PK

            # --- 5. GUARDAR ÍTEMS (Detalle) ---
            formset.instance = venta  # Asignar la venta a los ítems
            items = formset.save(commit=False)
            for item in items:
                # Si el precio no se modificó, usar el precio base del producto
                if not item.precio_unitario or int(item.precio_unitario) == 0:
                    item.precio_unitario = int(item.producto.precio_unitario)
                item.save()
            # Procesar ítems marcados para eliminar (en caso de edición, aunque aquí es creación)
            for del_form in formset.deleted_forms:
                if del_form.instance.pk:
                    del_form.instance.delete()
            formset.save_m2m() # Necesario si hubiera campos ManyToMany

            # --- 6. DESCONTAR STOCK POR FEFO ---
            for producto, cantidad_total in productos_a_descontar.items():
                ok = _descontar_por_FEFO(producto, cantidad_total) # Llamar a la función auxiliar
                if not ok:
                    # Si FEFO falla (stock inconsistente), revertir todo
                    messages.error(request, f"No fue posible descontar {cantidad_total} de {producto.nombre} (FEFO). Stock inconsistente.")
                    # Al estar en 'transaction.atomic', esto revierte la venta
                    raise ValueError("Error de FEFO: Stock inconsistente.") 

            # --- 7. RE-CALCULAR TOTAL (Buena práctica, por si acaso) ---
            venta.calcular_total() # Asumiendo que existe este método en el modelo Sale
            if venta.metodo_pago == "EFECTIVO":
                venta.cambio = int((venta.monto_pagado or 0)) - int(venta.total)
            else:
                venta.cambio = 0
            venta.save()

            messages.success(request, "Venta registrada correctamente.")
            return redirect("venta_detail", pk=venta.pk) # Redirigir al detalle de la venta

        else:
            # Si el formulario principal o el formset no son válidos
            messages.error(request, "Error en el formulario. Revisa los campos marcados.")

    else:
        # Petición GET: Mostrar formularios vacíos
        form = SaleForm(instance=venta)
        formset = SaleItemFormSet(instance=venta)

    return render(request, "ventas/form.html", {
        "form": form,
        "formset": formset,
        "precios": precios,
        "stock_map": json.dumps(stock_map)
    })


def venta_detalle(request, pk):
    """ Muestra el detalle de una venta específica ya creada. """
    venta = get_object_or_404(Sale, pk=pk)
    return render(request, "ventas/detail.html", {"venta": venta})


def venta_pdf(request, pk):
    """
    Genera un comprobante de venta en PDF usando ReportLab.
    """
    venta = get_object_or_404(Sale, pk=pk)
    
    # 1. Crear respuesta HTTP de tipo PDF
    response = HttpResponse(content_type='application/pdf')
    # Definir nombre del archivo (inline = se abre en navegador)
    response['Content-Disposition'] = f'inline; filename="venta_{venta.pk}.pdf"'
    
    # 2. Crear el "lienzo" (Canvas) de ReportLab sobre la respuesta
    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    x_margin, y_margin = 2 * cm, 2 * cm
    y = height - y_margin  # Posición Y actual (empieza arriba)

    # 3. Dibujar el contenido
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x_margin, y, "Comprobante de Venta")
    y -= 1.2 * cm  # Mover la 'y' hacia abajo

    c.setFont("Helvetica", 11)
    c.drawString(x_margin, y, f"Venta #{venta.pk}  |  Fecha: {venta.fecha.strftime('%d-%m-%Y %H:%M')}")
    y -= 0.6 * cm
    c.drawString(x_margin, y, f"Cliente: {venta.cliente.nombre}")
    y -= 0.4 * cm
    if venta.cliente.direccion:
        c.drawString(x_margin, y, f"Dirección: {venta.cliente.direccion}")
        y -= 0.4 * cm
    y -= 0.4 * cm

    # Cabecera de la tabla de ítems
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x_margin, y, "Producto")
    c.drawString(x_margin + 8 * cm, y, "Cant.")
    c.drawString(x_margin + 11 * cm, y, "P. Unit.")
    c.drawString(x_margin + 14 * cm, y, "Subtotal")
    y -= 0.5 * cm
    c.line(x_margin, y, width - x_margin, y)  # Línea horizontal
    y -= 0.3 * cm

    # Dibujar los ítems
    c.setFont("Helvetica", 10)
    for item in venta.items.select_related("producto").all():
        # Controlar salto de página si 'y' está muy abajo
        if y < 3 * cm:
            c.showPage()  # Terminar página actual, empezar una nueva
            y = height - y_margin  # Resetear 'y'
            c.setFont("Helvetica", 10) # Resetear fuente
        
        c.drawString(x_margin, y, item.producto.nombre[:40]) # Nombre (acortado)
        c.drawRightString(x_margin + 10 * cm, y, f"{float(item.cantidad):.3f}") # Cantidad (alineada derecha)
        c.drawRightString(x_margin + 13 * cm, y, f"${item.precio_unitario:,}".replace(",", ".")) # Precio
        c.drawRightString(width - x_margin, y, f"${int(item.subtotal):,}".replace(",", ".")) # Subtotal
        y -= 0.45 * cm

    # Dibujar el Total
    y -= 0.2 * cm
    c.line(x_margin, y, width - x_margin, y)
    y -= 0.6 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - x_margin, y, f"TOTAL: ${int(venta.total):,}".replace(",", "."))

    # 4. Finalizar y guardar el PDF
    c.showPage()
    c.save()
    return response