from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import categoria, producto, Carrito, ItemCarrito, cliente, pedido, detallepedido
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from django.utils.timezone import localtime
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
import random

#Views inicio.
def inicio(request):
    cache_key = 'productos_aleatorios_home'
    productos = cache.get(cache_key)
    
    if not productos:
        todos_productos_ids = list(producto.objects.values_list('id', flat=True))
        if len(todos_productos_ids) >= 8:
            ids_aleatorios = random.sample(todos_productos_ids, 8)
            productos = producto.objects.filter(id__in=ids_aleatorios)
            cache.set(cache_key, productos, 3600)
        else:
            productos = producto.objects.filter(stock__gt=0)[:6]
    
    return render(request, '1.inicio.html', {'productos': productos})

#Views categoria productos.
def categoria_productos(request, categoria_id, orden=None):
    categoria_actual = categoria.objects.get(id=categoria_id)
    productos_categoria = producto.objects.filter(categoria=categoria_actual)

    #ordenamiento.
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

#Views detalle productos.
def detalle_productos(request, producto_id): 
    producto_actual = producto.objects.get(id=producto_id) 
    return render(request, '3.detalle_productos.html', {'producto': producto_actual})

#Views busqueda.
def buscar_productos(request):
    query = request.GET.get('q', '')
    
    if query:
        productos = producto.objects.filter(
            Q(nombre__icontains=query) | 
            Q(descripcion__icontains=query) |
            Q(categoria__nombre__icontains=query)
        )
    else:
        productos = producto.objects.none()
    
    return render(request, '4.resultados_busqueda.html', {
        'productos': productos,
        'query': query
    })


#Views auxiliar del carrito.
def obtener_carrito(request):
    if not request.session.session_key:
        request.session.create()
    
    session_key = request.session.session_key
    carrito, created = Carrito.objects.get_or_create(session_key=session_key)
    return carrito



#Views Carro de compras.
def ver_carrito(request):
    carrito = obtener_carrito(request)
    items = carrito.itemcarrito_set.all().select_related('producto')

    total_items = items.aggregate(total=Sum('cantidad'))['total'] or 0
    request.session['cart_items_count'] = total_items
    
    subtotal_carrito = sum(item.subtotal() for item in items)
    
    context = {
        'carrito': carrito,
        'items': items,
        'subtotal_carrito': subtotal_carrito,
        'total_carrito': carrito.total() if items else 0
    }
    
    response = render(request, '5.carrito.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


# Views Agregar al carro de compras.
def agregar_al_carrito(request, producto_id):
    producto_obj = get_object_or_404(producto, id=producto_id)
    
    # VALIDAR STOCK ANTES DE AGREGAR
    if producto_obj.stock < 1:
        messages.error(request, f'❌ {producto_obj.nombre} está agotado')
        return redirect(request.META.get('HTTP_REFERER', 'inicio'))
    
    carrito = obtener_carrito(request)
    
    item, created = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto_obj,
        defaults={'precio': producto_obj.precio}
    )
    
    if not created:
        item.cantidad += 1
        item.save()
    
    total_items = carrito.itemcarrito_set.aggregate(total=Sum('cantidad'))['total'] or 0
    
    # Guardar en sesión para mostrar en todas las páginas
    request.session['cart_items_count'] = total_items
    
    # Redirigir con mensaje
    messages.success(request, f'¡{producto_obj.nombre} agregado al carrito!')
    return redirect(request.META.get('HTTP_REFERER', 'inicio'))



#Views Eliminar 
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    carrito = item.carrito
    
    item.delete()
    
    total_items = carrito.itemcarrito_set.aggregate(total=Sum('cantidad'))['total'] or 0
    request.session['cart_items_count'] = total_items
    
    messages.success(request, 'Producto eliminado del carrito')
    return redirect('ver_carrito')




#Actualizar cantidad de carrito
def actualizar_cantidad_carrito(request):
    if request.method == 'POST':
        try:
            item_id = request.POST.get('item_id')
            nueva_cantidad = int(request.POST.get('cantidad'))
            
            # Actualizar en BD
            item = ItemCarrito.objects.get(id=item_id)
            item.cantidad = nueva_cantidad
            item.save()
            
            # Recalcular totales REALES
            carrito = item.carrito
            subtotal_producto = item.subtotal()
            subtotal_carrito = sum(item.subtotal() for item in carrito.itemcarrito_set.all())
            total_carrito = carrito.total()
            
            return JsonResponse({
                'success': True,
                'subtotal_producto': float(subtotal_producto), 
                'subtotal_carrito': float(subtotal_carrito), 
                'total_carrito': float(total_carrito),       
                'item_id': item_id
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
        

        
#Views Obtener contador del carrito
def obtener_contador_carrito(request):
    carrito = obtener_carrito(request)
    total_items = carrito.itemcarrito_set.aggregate(total=Sum('cantidad'))['total'] or 0
    return JsonResponse({'count': total_items})


#Views checkout
def checkout(request):
    carrito = obtener_carrito(request)
    items = carrito.itemcarrito_set.all().select_related('producto')
    
    if not items:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('ver_carrito')
    
    subtotal_carrito = sum(item.subtotal() for item in items)
    total_carrito = subtotal_carrito
    
    context = {
        'items': items,
        'subtotal_carrito': subtotal_carrito,
        'total_carrito': total_carrito,
    }
    
    return render(request, '6.checkout.html', context)



# Views procesar pedido
def procesar_pedido(request):
    if request.method == 'POST':
        try:
            carrito = obtener_carrito(request)
            items = carrito.itemcarrito_set.all()
            
            # 1. VALIDAR CARRITO
            if not items:
                messages.error(request, 'Tu carrito está vacío')
                return redirect('ver_carrito')
            
            # 2. VALIDAR STOCK
            for item in items:
                if item.cantidad > item.producto.stock:
                    messages.error(request, f'No hay suficiente stock de {item.producto.nombre}')
                    return redirect('checkout')
            
            # 3. CREAR/OBTENER CLIENTE
            cliente_obj, created = cliente.objects.get_or_create(
                telefono=request.POST.get('telefono'),
                defaults={
                    'nombre': request.POST.get('nombre'),
                    'email': request.POST.get('email'),
                    'dirreccion': request.POST.get('direccion'),
                }
            )
            
            # 4. PROCESAR FECHA/HORA ENTREGA
            tipo_entrega = request.POST.get('tipo-entrega')
            fecha_entrega = None
            hora_entrega = None
            
            if tipo_entrega == 'express':
                fecha_entrega = timezone.now().date()
                hora_colombia = localtime(timezone.now() + timedelta(hours=1))
                hora_entrega = hora_colombia.time()
            else:
                # Programada: usar fecha/hora del formulario
                fecha_str = request.POST.get('fecha_entrega')
                hora_str = request.POST.get('hora_entrega')
                if fecha_str and hora_str:
                    fecha_entrega = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                    hora_entrega = datetime.strptime(hora_str, '%H:%M').time()
            
            # 5. CREAR PEDIDO
            pedido_obj = pedido.objects.create(
                cliente=cliente_obj,
                total=carrito.total(),
                estado='pendiente',
                
                # Sistema de entrega
                tipo_entrega=tipo_entrega,
                zona_entrega=request.POST.get('zona_entrega'),
                
                # Información de entrega
                direccion_entrega=request.POST.get('direccion'),
                ciudad=request.POST.get('ciudad', 'Cali'),
                instrucciones_entrega=request.POST.get('instrucciones', ''),
                
                # Sistema de pago
                metodo_pago=request.POST.get('metodo_pago', 'efectivo'),
                estado_pago='pendiente',
                
                # Campos de entrega (si existen)
                fecha_entrega=fecha_entrega,
                hora_entrega=hora_entrega,
            )
            
            # 6. CREAR DETALLES DEL PEDIDO
            for item in items:
                detallepedido.objects.create(
                    pedido=pedido_obj,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    subtotal=item.subtotal()
                )

            # 6.4 ACTUALIZAR STOCK DE PRODUCTOS
            for detalle in pedido_obj.detallepedido_set.all():
                producto_obj = detalle.producto
                producto_obj.stock -= detalle.cantidad
                producto_obj.save()

            # 6.5 LIMPIAR CARRITO
            carrito.itemcarrito_set.all().delete()
            request.session['cart_items_count'] = 0
            
            # 7. REDIRIGIR SEGÚN MÉTODO DE PAGO
            metodo_pago = request.POST.get('metodo_pago')
            
            if metodo_pago == 'efectivo':
                return redirect('confirmacion_pedido', pedido_id=pedido_obj.id)
            
            elif metodo_pago in ['nequi', 'daviplata',]:
                messages.success(request, f'Pedido creado. Método: {metodo_pago.upper()}')
                return redirect('confirmacion_pedido', pedido_id=pedido_obj.id)
                            
            else:
                # Método no reconocido
                messages.error(request, 'Método de pago no válido')
                return redirect('checkout')
            
        except Exception as e:
            messages.error(request, f'Error al procesar el pedido: {str(e)}')
            return redirect('checkout')
    
    return redirect('checkout')



# Views de confirmación de pedido
def confirmacion_pedido(request, pedido_id):
    pedido_obj = get_object_or_404(pedido, id=pedido_id)
    
    context = {
        'pedido': pedido_obj,
    }
    
    return render(request, '7.confirmacion_pedido.html', context)

# Views para verificar grupos de administrador
def es_administrador(user):
    return user.groups.filter(name='administrador').exists()

# Views de dashboard/admin
@login_required
@user_passes_test(es_administrador)
def dashboard_admin(request):
    pedidos = pedido.objects.all().order_by('-fecha')
    return render(request, '8.admin_dashboard.html', {'pedidos': pedidos})


# Views para verificar grupos de domiciliario
def es_domiciliario(user):
    return user.groups.filter(name='domiciliarios').exists()

# Views de dashboard/domiciliario
@login_required
@user_passes_test(es_domiciliario)
def dashboard_domiciliario(request):
    pedidos = pedido.objects.all().order_by('-fecha')
    domiciliarios = pedido.objects.exclude(domiciliario__isnull=True).values_list('domiciliario', flat=True).distinct()
    return render(request, '9.domiciliario_dashboard.html', {
        'pedidos': pedidos,
        'domiciliarios': domiciliarios
    })


# Views Marcar Pedido como Entregado
def marcar_entregado(request, pedido_id):
    pedido_obj = get_object_or_404(pedido, id=pedido_id)

    print(f"🔍 DEBUG marcar_entregado:")
    print(f"  Pedido ID: {pedido_id}")
    print(f"  Estado ANTES: {pedido_obj.estado}")
    print(f"  Estado_pago ANTES: {pedido_obj.estado_pago}")

    # VERIFICAR que no esté ya entregado
    if pedido_obj.estado == 'entregado':
        messages.warning(request, f'El pedido #{pedido_id} ya estaba marcado como entregado')
        return redirect('domiciliario_dashboard')
    
    # 2. Actualizar estado del pedido
    pedido_obj.estado = 'entregado'
    pedido_obj.estado_pago = 'pagado'
    pedido_obj.ubicacion_actual = 'Entregado'
    pedido_obj.save()
    
    messages.success(request, f'Pedido #{pedido_id} marcado como entregado')
    return redirect('domiciliario_dashboard')
        


# Views Asignar Domiciliario      
def asignar_domiciliario(request, pedido_id):
    if request.method == 'POST':
        pedido_obj = get_object_or_404(pedido, id=pedido_id)
        domiciliario_nombre = request.POST.get('domiciliario')
        
        pedido_obj.domiciliario = domiciliario_nombre
        pedido_obj.save()
        
        messages.success(request, f'Domiciliario {domiciliario_nombre} asignado al pedido #{pedido_id}')
        return redirect('dashboard_admin')
    

# Views Actualizar Estado del Pedido
def marcar_en_camino(request, pedido_id):
    pedido_obj = get_object_or_404(pedido, id=pedido_id)

    if pedido_obj.estado == 'En camino':
        messages.warning(request, f'El pedido #{pedido_id} ya estaba marcado como "En camino"')
        return redirect('domiciliario_dashboard')
    
    # Actualizar estado
    pedido_obj.ubicacion_actual = 'En camino'
    pedido_obj.estado = 'camino'
    pedido_obj.save()
    
    messages.success(request, f'Pedido #{pedido_id} marcado como "En camino"')
    return redirect('domiciliario_dashboard')
    

# Views Segumiento de Pedido
def seguimiento_pedido(request, pedido_id):
    pedido_obj = get_object_or_404(pedido, id=pedido_id)
    return render(request, '10.seguimiento_pedido.html', {'pedido': pedido_obj})

