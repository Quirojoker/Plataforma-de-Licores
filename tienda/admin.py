from django.contrib import admin
from .models import categoria, producto, cliente, pedido, detallepedido

#fecha: 12SEP2025 se activa el admin de Django
admin.site.register(categoria)
admin.site.register(producto)
admin.site.register(cliente)
admin.site.register(pedido)
admin.site.register(detallepedido)