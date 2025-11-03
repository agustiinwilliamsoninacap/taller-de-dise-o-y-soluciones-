from django import forms
from django.forms import inlineformset_factory
from .models import Product, Client, RawMaterial, Recipe, RecipeItem, Sale, SaleItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["nombre", "categoria", "unidad", "precio_unitario", "activo"]

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["nombre", "email", "telefono", "direccion"]

class RawMaterialForm(forms.ModelForm):
    class Meta:
        model = RawMaterial
        fields = ["nombre", "unidad", "costo_unitario", "stock"]

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["nombre", "producto_final", "rendimiento_unidades"]

from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, RecipeItem

RecipeItemFormSet = inlineformset_factory(
    Recipe,
    RecipeItem,
    fields=["materia_prima", "cantidad"],
    widgets={"cantidad": forms.NumberInput(attrs={"step": "0.001", "min": "0"})},
    extra=0,          # 👈 sin filas iniciales
    can_delete=True,
    min_num=1,        # 👈 al menos 1 ítem para poder guardar
    validate_min=True
)



class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["cliente", "metodo_pago", "monto_pagado"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cliente no requerido (venta sin cliente)
        self.fields["cliente"].required = False
        # Monto pagado solo será requerido en vista si es EFECTIVO (lo validamos en la view)
        self.fields["monto_pagado"].required = False

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ["producto", "cantidad", "precio_unitario"]

# Aumenta número de filas iniciales visibles
SaleItemFormSet = inlineformset_factory(
    Sale, SaleItem, form=SaleItemForm, extra=3, can_delete=True
)

class ProductionForm(forms.Form):
    multiplicador = forms.DecimalField(min_value=0.001, decimal_places=3, initial=1, help_text="Cuántas veces ejecutar la receta")
    codigo_lote = forms.CharField(max_length=50)
    fecha_produccion = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    fecha_vencimiento = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))