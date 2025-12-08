from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('categoria/<int:categoria_id>/', views.categoria_productos, name='categoria_productos'),
    path('categoria/<int:categoria_id>/orden/<str:orden>/', views.categoria_productos, name='categoria_productos_orden'),
    path('producto/<int:producto_id>/', views.detalle_productos, name='detalle_productos'),
    path('buscar/', views.buscar_productos, name='buscar'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar-carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('actualizar-cantidad/', views.actualizar_cantidad_carrito, name='actualizar_cantidad'),
    path('api/cart-count/', views.obtener_contador_carrito, name='cart_count'),
    path('checkout/', views.checkout, name='checkout'),
    path('procesar-pedido/', views.procesar_pedido, name='procesar_pedido'),
    path('confirmacion-pedido/<int:pedido_id>/', views.confirmacion_pedido, name='confirmacion_pedido'),
    path('admin-dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('marcar-entregado/<int:pedido_id>/', views.marcar_entregado, name='marcar_entregado'),
    path('asignar-domiciliario/<int:pedido_id>/', views.asignar_domiciliario, name='asignar_domiciliario'),
    path('domiciliario-dashboard/', views.dashboard_domiciliario, name='domiciliario_dashboard'),
    path('seguimiento/<int:pedido_id>/', views.seguimiento_pedido, name='seguimiento_pedido'),
    path('marcar-en-camino/<int:pedido_id>/', views.marcar_en_camino, name='marcar_en_camino'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='11.login.html',redirect_authenticated_user=True), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('contacto/', views.contacto, name='contacto'),
]

