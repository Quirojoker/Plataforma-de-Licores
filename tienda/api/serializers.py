from rest_framework import serializers
from tienda.models import categoria, producto, ImagenProducto, detallepedido, pedido

# Serializers define the API representation.

# Categoria Serializer
class categoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = categoria
        fields = ['id', 'nombre', 'descripcion',]

# Detalle imagenes producto Serializer
class ImagenProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenProducto
        fields = ['id', 'imagen', 'orden',]

# Producto Serializer
class productoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)

    imagenes_detalle = ImagenProductoSerializer(source='imagenproducto_set', many=True, read_only=True)

    class Meta:
        model = producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'imagen', 'imagenes_detalle', 'categoria', 'categoria_nombre', 'keywords',]


# Detalle del pedido Serializer
class detallepedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = detallepedido
        fields = ['producto', 'cantidad']


# Pedido Create Serializer
class pedidocreateSerializer(serializers.Serializer):
    # Cliente
    nombre = serializers.CharField()
    telefono = serializers.CharField()
    email = serializers.EmailField(required=False, allow_null=True)
    direccion = serializers.CharField()

    # Entrega
    tipo_entrega = serializers.ChoiceField(choices=['express', 'programada'])
    zona_entrega = serializers.ChoiceField(choices=['norte', 'sur', 'oriente', 'occidente', 'centro'])
    fecha_entrega = serializers.DateField(required=False)
    hora_entrega = serializers.TimeField(required=False)

    # Productos
    items = detallepedidoSerializer(many=True)

    # Extras
    instrucciones_entrega = serializers.CharField(required=False, allow_blank=True)


# Seguimiento Pedido Serializer
class seguimientopedidoSerializer(serializers.ModelSerializer):

    estado_display = serializers.CharField(source='get_estado_display', read_only=True)


    fecha = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    fecha_actualizacion = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    hora_entrega = serializers.TimeField(format="%H:%M")
    total = serializers.DecimalField(max_digits=10, decimal_places=0)
    
    class Meta:
        model = pedido
        fields = [
            'codigo_seguimiento',
            'estado',
            'estado_display',
            'ubicacion_actual',
            'tipo_entrega',
            'fecha',
            'fecha_entrega',
            'hora_entrega',
            'total',
            'fecha_actualizacion',
            'domiciliario',
        ]