from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
import re
from datetime import date, timedelta
from django.utils import timezone
from rest_framework import status
from tienda.models import categoria, producto, cliente, pedido, detallepedido
from .serializers import categoriaSerializer, productoSerializer, pedidocreateSerializer, detallepedidoSerializer, seguimientopedidoSerializer


#Views API

#Views de prueba
@api_view(['GET'])
def ping(request):
    return Response({"status": "ok"})


#Lista categorias
@api_view(['GET'])
def lista_categorias(request):
    categorias = categoria.objects.all()
    serializer = categoriaSerializer(categorias, many=True)
    return Response(serializer.data)


#Lista productos
@api_view(['GET'])
def lista_productos(request):
    productos = producto.objects.filter(stock__gt=0)

    categoria_id = request.GET.get('categoria')

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
        
    serializer = productoSerializer(productos, many=True)
    return Response(serializer.data)


#Detalle producto
@api_view(['GET'])
def detalle_producto(request, producto_id):
    try:
        producto_obj = producto.objects.get(id=producto_id, stock__gt=0)

    except producto.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=404)

    serializer = productoSerializer(producto_obj)
    return Response(serializer.data)


#Busqueda de productos
@api_view(['GET'])
def buscar_productos(request):
    query = request.GET.get('q')

    if not query:
        return Response({"error": "Debe enviar ?q="}, status=400)

    q = query.lower().strip()

    variantes = set()
    variantes.add(q)

    if q.endswith('s'):
        variantes.add(q[:-1])
    if q.endswith('es'):
        variantes.add(q[:-2])

    filtros = Q(stock__gt=0)

    texto = Q()
    for palabra in variantes:
        texto |= Q(nombre__icontains=palabra)
        texto |= Q(descripcion__icontains=palabra)
        texto |= Q(keywords__icontains=palabra)

    productos = producto.objects.filter(filtros & texto).distinct()

    serializer = productoSerializer(productos, many=True)
    return Response(serializer.data)



#Crear pedido
@api_view(['POST'])
def crear_pedido(request):
    serializer = pedidocreateSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    data = serializer.validated_data

    #Validar tipo de entrega
    tipo_entrega = data['tipo_entrega']

    if tipo_entrega == 'express':
        ahora = timezone.localtime(timezone.now())
        entrega = ahora + timedelta(minutes=60)

        fecha_entrega = entrega.date()
        hora_entrega = entrega.time()
    else:
        fecha_entrega = data.get('fecha_entrega')
        hora_entrega = data.get('hora_entrega')

    if tipo_entrega == 'programada':
        if not data.get('fecha_entrega') or not data.get('hora_entrega'):
            return Response(
                {"error": "La entrega programada requiere fecha y hora"},
                status=400
            )

        if data['fecha_entrega'] < date.today() + timedelta(days=2):
            return Response(
                {"error": "La entrega programada debe ser mínimo en 48 horas"},
                status=400
            )

    #Crear cliente
    cliente_obj, _ = cliente.objects.get_or_create(
        telefono=data['telefono'],
        defaults={
            'nombre': data['nombre'],
            'email': data.get('email'),
            'dirreccion': data['direccion']
        }
    )

    #Crear pedido
    pedido_obj = pedido.objects.create(
        cliente=cliente_obj,
        tipo_entrega=tipo_entrega,
        zona_entrega=data['zona_entrega'],
        fecha_entrega=fecha_entrega,
        hora_entrega=hora_entrega,
        direccion_entrega=data['direccion'],
        instrucciones_entrega=data.get('instrucciones_entrega', ''),
        total=0
    )

    total = 0

    #Detalle del pedido
    for item in data['items']:
        producto_obj = producto.objects.get(id=item['producto'].id)

        if producto_obj.stock < item['cantidad']:
            return Response(
                {"error": f"Stock insuficiente para {producto_obj.nombre}"},
                status=400
            )

        subtotal = producto_obj.precio * item['cantidad']
        total += subtotal

        detallepedido.objects.create(
            pedido=pedido_obj,
            producto=producto_obj,
            cantidad=item['cantidad'],
            subtotal=subtotal
        )

        # Descontar stock
        producto_obj.stock -= item['cantidad']
        producto_obj.save()

    detalles = detallepedido.objects.filter(pedido=pedido_obj)

    productos_respuesta = []

    for d in detalles:
        productos_respuesta.append({
            "id": d.producto.id,
            "nombre": d.producto.nombre,
            "cantidad": d.cantidad,
            "precio_unitario": float(d.producto.precio),
            "subtotal": float(d.subtotal)
        })


    #Actualizar total del pedido
    pedido_obj.total = total
    pedido_obj.save()

    return Response({
        'mensaje': 'Pedido creado correctamente',
        'pedido_id': pedido_obj.id,
        'tipo_entrega': pedido_obj.tipo_entrega,
        'fecha_entrega': pedido_obj.fecha_entrega,
        'hora_entrega': (pedido_obj.hora_entrega).strftime("%H:%M") if pedido_obj.hora_entrega else None,
        'instrucciones_entrega': pedido_obj.instrucciones_entrega,
        'codigo_seguimiento': pedido_obj.codigo_seguimiento,
        'productos': productos_respuesta,
        'total': total
    }, status=201)


#Seguimiento pedido
@api_view(['GET'])
def seguimiento_pedido(request, codigo):
    try:
        pedido_obj = pedido.objects.get(codigo_seguimiento=codigo)
    except pedido.DoesNotExist:
        return Response(
            {"error": "Código de seguimiento inválido"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = seguimientopedidoSerializer(pedido_obj)
    return Response(serializer.data)