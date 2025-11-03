from django.contrib import admin
from .models import Category, Product, Client, RawMaterial, Recipe, RecipeItem, Sale, SaleItem, ProductBatch

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "unidad", "precio_unitario", "stock", "activo")
    list_filter = ("categoria", "activo")
    search_fields = ("nombre",)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email", "telefono")
    search_fields = ("nombre", "email")

@admin.register(RawMaterial)
class RawMaterialAdmin(admin.ModelAdmin):
    list_display = ("nombre", "unidad", "costo_unitario", "stock")
    search_fields = ("nombre",)

class RecipeItemInline(admin.TabularInline):
    model = RecipeItem
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeItemInline]
    list_display = ("nombre", "producto_final", "rendimiento_unidades")

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    inlines = [SaleItemInline]
    list_display = ("id", "cliente", "fecha", "total")

@admin.register(ProductBatch)
class ProductBatchAdmin(admin.ModelAdmin):
    list_display = ("producto", "codigo_lote", "fecha_produccion", "fecha_vencimiento", "cantidad")
    list_filter = ("producto", "fecha_vencimiento")
    search_fields = ("codigo_lote",)
