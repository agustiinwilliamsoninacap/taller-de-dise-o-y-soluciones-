from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Productos
    path('productos/', views.ProductListView.as_view(), name='productos_list'),
    path('productos/nuevo/', views.ProductCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', views.ProductUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/eliminar/', views.ProductDeleteView.as_view(), name='producto_delete'),

    # Clientes
    path('clientes/', views.ClientListView.as_view(), name='clientes_list'),
    path('clientes/nuevo/', views.ClientCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.ClientUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', views.ClientDeleteView.as_view(), name='cliente_delete'),
    path('clientes/<int:pk>/', views.cliente_detalle, name='cliente_detalle'),

    # Ventas
    path('ventas/', views.SaleListView.as_view(), name='ventas_list'),
    path('ventas/nueva/', views.venta_crear, name='venta_create'),
    path('ventas/<int:pk>/', views.venta_detalle, name='venta_detail'),
    path('ventas/<int:pk>/pdf/', views.venta_pdf, name='venta_pdf'),

    # Materias primas
    path('materias/', views.RawMaterialListView.as_view(), name='materias_list'),
    path('materias/nueva/', views.RawMaterialCreateView.as_view(), name='materia_create'),
    path('materias/<int:pk>/editar/', views.RawMaterialUpdateView.as_view(), name='materia_update'),
    path('materias/<int:pk>/eliminar/', views.RawMaterialDeleteView.as_view(), name='materia_delete'),

    # Recetas
    path('recetas/', views.RecipeListView.as_view(), name='recetas_list'),
    path('recetas/nueva/', views.receta_crear, name='receta_create'),
    path('recetas/<int:pk>/', views.receta_detalle, name='receta_detail'),
    path('recetas/<int:pk>/editar/', views.receta_editar, name='receta_update'),
    path('recetas/<int:pk>/producir/', views.receta_producir, name='receta_producir'),
]
