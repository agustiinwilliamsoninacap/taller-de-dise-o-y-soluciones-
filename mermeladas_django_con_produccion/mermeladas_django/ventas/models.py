from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator

class Category(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

UNIT_CHOICES = [
    ("g", "Gramos (g)"),
    ("kg", "Kilogramos (kg)"),
    ("ml", "Mililitros (ml)"),
    ("l", "Litros (L)"),
    ("un", "Unidad (un)"),
]

class Product(models.Model):
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    unidad = models.CharField(max_length=2, choices=UNIT_CHOICES, default="un")
    precio_unitario = models.IntegerField(validators=[MinValueValidator(0)], help_text="Precio de venta por unidad (CLP entero)")
    stock = models.IntegerField(default=0, help_text="Stock disponible en unidades enteras")
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('productos_list')

class RawMaterial(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    unidad = models.CharField(max_length=2, choices=UNIT_CHOICES, default="g")
    costo_unitario = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Costo por unidad (CLP entero)")
    stock = models.IntegerField(default=0, help_text="Stock disponible en unidades enteras")

    class Meta:
        verbose_name = "Materia Prima"
        verbose_name_plural = "Materias Primas"

    def __str__(self):
        return self.nombre

class Client(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nombre

    def total_gastado(self):
        from django.db.models import Sum
        # Cambiamos venta_set -> sale_set (nombre real del modelo)
        return self.sale_set.aggregate(total=Sum('total'))['total'] or 0

class Recipe(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    producto_final = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    rendimiento_unidades = models.DecimalField(max_digits=12, decimal_places=3, default=1)

    class Meta:
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"

    def __str__(self):
        return self.nombre

    def costo_estandar(self):
        return sum(item.cantidad * item.materia_prima.costo_unitario for item in self.items.all())

class RecipeItem(models.Model):
    receta = models.ForeignKey(Recipe, related_name="items", on_delete=models.CASCADE)
    materia_prima = models.ForeignKey(RawMaterial, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)

    class Meta:
        verbose_name = "Ingrediente de Receta"
        verbose_name_plural = "Ingredientes de Receta"

    def __str__(self):
        return f"{self.materia_prima} ({self.cantidad})"

class ProductBatch(models.Model):
    producto = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="lotes")
    codigo_lote = models.CharField(max_length=50)
    fecha_produccion = models.DateField()
    fecha_vencimiento = models.DateField()
    cantidad = models.DecimalField(max_digits=12, decimal_places=3, default=0)

    class Meta:
        verbose_name = "Lote de Producto"
        verbose_name_plural = "Lotes de Producto"
        ordering = ["fecha_vencimiento", "fecha_produccion", "id"]

    def __str__(self):
        return f"{self.producto} | Lote {self.codigo_lote} | vence {self.fecha_vencimiento}"

from django.core.validators import MinValueValidator

PAYMENT_CHOICES = [
    ("EFECTIVO", "Efectivo"),
    ("TRANSFERENCIA", "Transferencia"),
    ("DEBITO", "Débito"),
    ("CREDITO", "Crédito"),
]

class Sale(models.Model):
    # Permitir venta sin cliente
    cliente = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True)

    fecha = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField(default=0)

    # Campos de pago
    metodo_pago = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="EFECTIVO")
    monto_pagado = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    cambio = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ["-fecha"]

    def __str__(self):
        return f"Venta #{self.pk} - {self.cliente or 'Sin cliente'}"

    def calcular_total(self):
        self.total = sum(int(item.subtotal) for item in self.items.all())
        return self.total

class SaleItem(models.Model):
    venta = models.ForeignKey(Sale, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey(Product, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=12, decimal_places=3)
    precio_unitario = models.IntegerField(validators=[MinValueValidator(0)])
    subtotal = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Ítem de Venta"
        verbose_name_plural = "Ítems de Venta"

    def save(self, *args, **kwargs):
        self.subtotal = int((self.precio_unitario or 0) * float(self.cantidad or 0))
        super().save(*args, **kwargs)

