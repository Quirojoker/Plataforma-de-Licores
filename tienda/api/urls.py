from django.urls import path
from .views import ping, lista_categorias, lista_productos, detalle_producto, buscar_productos, crear_pedido, seguimiento_pedido

urlpatterns = [
    path('ping/', ping),
    path('categorias/', lista_categorias),
    path('productos/', lista_productos),
    path('productos/<int:producto_id>/', detalle_producto),
    path('productos/buscar/', buscar_productos),
    path('pedidos/crear/', crear_pedido),
    path('seguimiento/<str:codigo>/', seguimiento_pedido),
]