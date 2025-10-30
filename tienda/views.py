from django.shortcuts import render
from .models import categoria, producto

def inicio(request):
    return render(request, '1.inicio.html')

def categoria_productos(request, categoria_id, orden=None):
    categoria_actual = categoria.objects.get(id=categoria_id)
    productos_categoria = producto.objects.filter(categoria=categoria_actual)

    #ordenamiento
    if orden == 'nombre':
        productos_categoria = productos_categoria.order_by ('nombre')
    elif orden == 'precio_asc':
        productos_categoria = productos_categoria.order_by('precio')
    elif orden == 'precio_desc':
        productos_categoria = productos_categoria.order_by('-precio')
    else:
        productos_categoria = productos_categoria.order_by('id')

    return render(request, '2.categoria_productos.html', {
        'categoria': categoria_actual,
        'productos': productos_categoria,
        'orden_actual': orden
    })