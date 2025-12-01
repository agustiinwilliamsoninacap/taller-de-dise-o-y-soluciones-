# --- Importaciones ---
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db import transaction
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from django.db.models.deletion import ProtectedError
import json
from django.utils import timezone

# Importar modelos y formularios
from .models import Product, Client, RawMaterial, Recipe, RecipeItem, Sale, SaleItem, ProductBatch
from .forms import ProductForm, ClientForm, RawMaterialForm, RecipeForm, RecipeItemFormSet, SaleForm, SaleItemFormSet, \
    ProductionForm


# --- Vistas Principales ---

def home(request):
    """ Vista principal (Dashboard). """
    datos = {
        "total_productos": Product.objects.count(),
        "total_clientes": Client.objects.count(),
        "total_ventas": Sale.objects.count(),
    }
    return render(request, "home.html", datos)


# --- Sección: Productos ---

class ProductListView(ListView):
    model = Product
    template_name = "productos/list.html"
    context_object_name = "productos"


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "productos/form.html"
    success_url = reverse_lazy("productos_list")


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "productos/form.html"
    success_url = reverse_lazy("productos_list")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("productos_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            sales_count = self.object.saleitem_set.count()
            recipes_count = self.object.recipe_set.count()
            messages.error(request,
                           f"No se puede eliminar '{self.object.nombre}', está en {sales_count} ventas y {recipes_count} recetas.")
            return redirect(self.success_url)


# --- Sección: Clientes ---

class ClientListView(ListView):
    model = Client
    template_name = "clientes/list.html"
    context_object_name = "clientes"


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = "clientes/form.html"
    success_url = reverse_lazy("clientes_list")


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "clientes/form.html"
    success_url = reverse_lazy("clientes_list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("clientes_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            sales_count = self.object.sale_set.count()
            messages.error(request,
                           f"No se puede eliminar '{self.object.nombre}' porque tiene {sales_count} venta(s) asociada(s).")
            return redirect(self.success_url)


def cliente_detalle(request, pk):
    cliente = get_object_or_404(Client, pk=pk)
    from django.db.models import Sum
    cliente.total_gastado = Sale.objects.filter(cliente=cliente).aggregate(total=Sum('total'))['total'] or 0
    ventas = Sale.objects.filter(cliente=cliente).prefetch_related("items", "items__producto")
    return render(request, "clientes/detail.html", {"cliente": cliente, "ventas": ventas})


# --- Sección: Materias Primas ---

class RawMaterialListView(ListView):
    model = RawMaterial
    template_name = "materias/list.html"
    context_object_name = "materias"


class RawMaterialCreateView(CreateView):
    model = RawMaterial
    form_class = RawMaterialForm
    template_name = "materias/form.html"
    success_url = reverse_lazy("materias_list")


class RawMaterialUpdateView(UpdateView):
    model = RawMaterial
    form_class = RawMaterialForm
    template_name = "materias/form.html"
    success_url = reverse_lazy("materias_list")


class RawMaterialDeleteView(DeleteView):
    model = RawMaterial
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("materias_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            recetas = self.object.recipeitem_set.select_related("receta")
            nombres = ", ".join(sorted({ri.receta.nombre for ri in recetas}))
            messages.error(request, f"No se puede eliminar '{self.object.nombre}' porque se usa en recetas: {nombres}.")
            return redirect(self.success_url)


# --- Sección: Recetas ---

class RecipeListView(ListView):
    model = Recipe
    template_name = "recetas/list.html"
    context_object_name = "recetas"


@transaction.atomic
def receta_crear(request):
    """
    Vista para CREAR una nueva receta con sus ingredientes.
    Esta es la función que te faltaba y causaba el error.
    """
    unidades = {m.pk: m.unidad for m in RawMaterial.objects.all()}

    if request.method == "POST":
        form = RecipeForm(request.POST)
        formset = RecipeItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            receta = form.save()  # Guarda primero la cabecera para tener ID
            formset.instance = receta  # Asocia los ingredientes a esa receta
            formset.save()  # Guarda los ingredientes
            messages.success(request, "Receta creada exitosamente.")
            return redirect("recetas_list")
        else:
            messages.error(request, "Error al crear la receta. Revise los datos.")
    else:
        form = RecipeForm()
        formset = RecipeItemFormSet()

    return render(request, "recetas/form.html", {
        "form": form,
        "formset": formset,
        "unidades": json.dumps(unidades)
    })


@transaction.atomic
def receta_editar(request, pk):
    """ Vista para editar Receta y sus ingredientes. """
    receta = get_object_or_404(Recipe, pk=pk)
    unidades = {m.pk: m.unidad for m in RawMaterial.objects.all()}

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=receta)
        formset = RecipeItemFormSet(request.POST, instance=receta)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Receta actualizada correctamente.")
            return redirect("recetas_list")
        else:
            messages.error(request, "Error al actualizar la receta.")
    else:
        form = RecipeForm(instance=receta)
        formset = RecipeItemFormSet(instance=receta)

    return render(request, "recetas/form.html", {
        "form": form,
        "formset": formset,
        "unidades": json.dumps(unidades)
    })


@transaction.atomic
def receta_producir(request, pk):
    """
    Vista para "producir" una receta.
    Genera el CODIGO DE LOTE automáticamente e ignora el input manual.
    """
    receta = get_object_or_404(Recipe, pk=pk)
    if not receta.producto_final:
        messages.error(request, "Esta receta no tiene producto final asignado.")
        return redirect("receta_detail", pk=pk)

    if request.method == "POST":
        form = ProductionForm(request.POST)

        if form.is_valid():
            # Obtener datos del formulario
            mult = form.cleaned_data["multiplicador"]
            fprod = form.cleaned_data["fecha_produccion"]
            fven = form.cleaned_data["fecha_vencimiento"]

            # --- GENERACIÓN AUTOMÁTICA DEL CÓDIGO ---
            # Formato: L{ID_PRODUCTO}-{FECHA_HORA_MINUTO}
            ahora = timezone.now()
            cod = f"L{receta.producto_final.id}-{ahora.strftime('%d%m%y%H%M')}"
            # ----------------------------------------

            # 1. Verificar stock de materias primas
            faltantes = []
            for item in receta.items.select_related("materia_prima"):
                req = item.cantidad * mult
                if item.materia_prima.stock < req:
                    faltantes.append(
                        f"{item.materia_prima.nombre} (requiere {req}, disponible {item.materia_prima.stock})")

            if faltantes:
                messages.error(request, "Stock insuficiente: " + "; ".join(faltantes))
                return redirect("receta_detail", pk=pk)

            # 2. Descontar stock de materias primas
            for item in receta.items.select_related("materia_prima"):
                req = item.cantidad * mult
                mp = item.materia_prima
                mp.stock = mp.stock - req
                mp.save()

            # 3. Crear el Lote con el CÓDIGO AUTOMÁTICO
            unidades = receta.rendimiento_unidades * mult
            ProductBatch.objects.create(
                producto=receta.producto_final,
                codigo_lote=cod,
                fecha_produccion=fprod,
                fecha_vencimiento=fven,
                cantidad=unidades
            )

            # 4. Actualizar el stock total
            producto = receta.producto_final
            producto.stock = sum(lote.cantidad for lote in producto.lotes.filter(cantidad__gt=0))
            producto.save()

            messages.success(request, f"Producción registrada: +{unidades} {producto.unidad}. Lote generado: {cod}")
            return redirect("receta_detail", pk=pk)
    else:
        form = ProductionForm()

    return render(request, "recetas/produccion_form.html", {"form": form, "receta": receta})


def receta_detalle(request, pk):
    """ Muestra el detalle de una receta. """
    receta = get_object_or_404(Recipe, pk=pk)
    return render(request, "recetas/detail.html", {"receta": receta})


# --- Helper de FEFO (First Expiring, First Out) ---

def _descontar_por_FEFO(producto, cantidad):
    """ Descuenta stock empezando por los lotes que vencen antes. """
    restante = float(cantidad)
    lotes = list(producto.lotes.filter(cantidad__gt=0).order_by("fecha_vencimiento", "fecha_produccion", "id"))

    stock_en_lotes = sum(l.cantidad for l in lotes)
    if stock_en_lotes < restante:
        producto.stock = stock_en_lotes
        producto.save()
        return False

    for lote in lotes:
        if restante <= 0:
            break
        disp = float(lote.cantidad)
        tomar = min(disp, restante)
        lote.cantidad = disp - tomar
        lote.save()
        restante -= tomar

    producto.stock = sum(l.cantidad for l in producto.lotes.filter(cantidad__gt=0))
    producto.save()

    return restante <= 0.0001


# --- Sección: Ventas ---

class SaleListView(ListView):
    model = Sale
    template_name = "ventas/list.html"
    context_object_name = "ventas"


@transaction.atomic
def venta_crear(request):
    """ Vista para crear una nueva Venta (con validación de stock y FEFO). """
    venta = Sale()
    productos = Product.objects.filter(activo=True, stock__gt=0)
    precios = {p.id: int(p.precio_unitario) for p in productos}
    stock_map = {p.id: float(p.stock) for p in productos}

    if request.method == "POST":
        form = SaleForm(request.POST, instance=venta)
        formset = SaleItemFormSet(request.POST, instance=venta)

        if form.is_valid() and formset.is_valid():
            total_provisional = 0
            productos_a_descontar = {}

            # 1. Validar ítems
            for f in formset.forms:
                if not f.cleaned_data or f.cleaned_data.get("DELETE"):
                    continue

                producto = f.cleaned_data.get("producto")
                cantidad = f.cleaned_data.get("cantidad")

                if not producto or not cantidad:
                    messages.error(request, "Se detectó una fila vacía. Complétela o bórrela.")
                    return render(request, "ventas/form.html", {"form": form, "formset": formset, "precios": precios,
                                                                "stock_map": json.dumps(stock_map)})

                productos_a_descontar[producto] = productos_a_descontar.get(producto, 0) + cantidad
                precio = f.cleaned_data.get("precio_unitario") or int(producto.precio_unitario)
                total_provisional += int(precio) * float(cantidad)

            if not productos_a_descontar:
                messages.error(request, "No se puede registrar una venta sin productos.")
                return render(request, "ventas/form.html", {"form": form, "formset": formset, "precios": precios,
                                                            "stock_map": json.dumps(stock_map)})

            # 2. Validar stock total
            for producto, cantidad_total in productos_a_descontar.items():
                if cantidad_total > producto.stock:
                    messages.error(request,
                                   f"Stock insuficiente para {producto.nombre}. Solicitado: {cantidad_total}, Disponible: {producto.stock}.")
                    return render(request, "ventas/form.html", {"form": form, "formset": formset, "precios": precios,
                                                                "stock_map": json.dumps(stock_map)})

            # 3. Validar pago
            metodo = form.cleaned_data.get("metodo_pago")
            pagado = form.cleaned_data.get("monto_pagado") or 0
            if metodo == "EFECTIVO" and int(pagado) < int(total_provisional):
                messages.error(request, f"Monto pagado insuficiente. Total: ${int(total_provisional)}.")
                return render(request, "ventas/form.html", {"form": form, "formset": formset, "precios": precios,
                                                            "stock_map": json.dumps(stock_map)})

            # 4. Guardar Venta
            venta = form.save(commit=False)
            venta.total = int(total_provisional)
            venta.cambio = int(pagado) - int(venta.total) if metodo == "EFECTIVO" else 0
            venta.save()

            # 5. Guardar Ítems
            formset.instance = venta
            items = formset.save(commit=False)
            for item in items:
                if not item.precio_unitario or int(item.precio_unitario) == 0:
                    item.precio_unitario = int(item.producto.precio_unitario)
                item.save()
            for del_form in formset.deleted_forms:
                if del_form.instance.pk:
                    del_form.instance.delete()
            formset.save_m2m()

            # 6. Descontar Stock (FEFO)
            for producto, cantidad_total in productos_a_descontar.items():
                ok = _descontar_por_FEFO(producto, cantidad_total)
                if not ok:
                    messages.error(request, f"Error de stock (FEFO) en {producto.nombre}.")
                    raise ValueError("Stock inconsistente FEFO")

            messages.success(request, "Venta registrada correctamente.")
            return redirect("venta_detail", pk=venta.pk)

        else:
            messages.error(request, "Error en el formulario. Revisa los campos.")

    else:
        form = SaleForm(instance=venta)
        formset = SaleItemFormSet(instance=venta)

    return render(request, "ventas/form.html", {
        "form": form,
        "formset": formset,
        "precios": precios,
        "stock_map": json.dumps(stock_map)
    })


def venta_detalle(request, pk):
    venta = get_object_or_404(Sale, pk=pk)
    return render(request, "ventas/detail.html", {"venta": venta})


def venta_pdf(request, pk):
    """ Genera PDF de la venta. """
    venta = get_object_or_404(Sale, pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="venta_{venta.pk}.pdf"'

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    x_margin, y_margin = 2 * cm, 2 * cm
    y = height - y_margin

    c.setFont("Helvetica-Bold", 14)
    c.drawString(x_margin, y, "Comprobante de Venta")
    y -= 1.2 * cm

    c.setFont("Helvetica", 11)
    c.drawString(x_margin, y, f"Venta #{venta.pk}  |  Fecha: {venta.fecha.strftime('%d-%m-%Y %H:%M')}")
    y -= 0.6 * cm
    c.drawString(x_margin, y, f"Cliente: {venta.cliente.nombre}")
    y -= 0.4 * cm
    if venta.cliente.direccion:
        c.drawString(x_margin, y, f"Dirección: {venta.cliente.direccion}")
        y -= 0.4 * cm
    y -= 0.4 * cm

    c.setFont("Helvetica-Bold", 10)
    c.drawString(x_margin, y, "Producto")
    c.drawString(x_margin + 8 * cm, y, "Cant.")
    c.drawString(x_margin + 11 * cm, y, "P. Unit.")
    c.drawString(x_margin + 14 * cm, y, "Subtotal")
    y -= 0.5 * cm
    c.line(x_margin, y, width - x_margin, y)
    y -= 0.3 * cm

    c.setFont("Helvetica", 10)
    for item in venta.items.select_related("producto").all():
        if y < 3 * cm:
            c.showPage()
            y = height - y_margin
            c.setFont("Helvetica", 10)

        c.drawString(x_margin, y, item.producto.nombre[:40])
        c.drawRightString(x_margin + 10 * cm, y, f"{float(item.cantidad):.3f}")
        c.drawRightString(x_margin + 13 * cm, y, f"${item.precio_unitario:,}".replace(",", "."))
        c.drawRightString(width - x_margin, y, f"${int(item.subtotal):,}".replace(",", "."))
        y -= 0.45 * cm

    y -= 0.2 * cm
    c.line(x_margin, y, width - x_margin, y)
    y -= 0.6 * cm
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - x_margin, y, f"TOTAL: ${int(venta.total):,}".replace(",", "."))

    c.showPage()
    c.save()
    return response
