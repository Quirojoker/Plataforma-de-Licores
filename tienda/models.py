from django.db import models

#fecha: 12SEP2025 se crean modelos para la tienda.

#categorias (cervezas comerciales, cervezas artesanales, vinos comerciales, vinos artesanales, licores).
class categoria (models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen_banner = models.ImageField(upload_to='categorias/', blank=True, null=True)
    texto_superpuesto = models.CharField(max_length=200, blank=True)
    descripcion_larga = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    
#prouctos
class producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveBigIntegerField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)#pendiente definir urls banco de img.
    categoria = models.ForeignKey(categoria, on_delete=models.CASCADE)
    en_promocion = models.BooleanField(default=False)
    precio_promocional = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_excesivo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'NOMBRE: {self.nombre} - PRECIO: {self.precio} - CANTIDA DISPONIBLE: {self.stock}'
    
#imagenes detalle del producto
class ImagenProducto(models.Model):
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/')
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"
    

# Carrito temporal (antes del pedido)
class Carrito(models.Model):
    session_key = models.CharField(max_length=100, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Carrito {self.id} - Sesión: {self.session_key}"
    
    def total(self):
        return sum(item.subtotal() for item in self.itemcarrito_set.all())
    
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio al momento de agregar
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
    def subtotal(self):
        return self.cantidad * self.precio
    
#clientes
class cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    dirreccion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'CLIENTE: {self.nombre} - TELEFONO: {self.telefono} - DIRRECCIÓN: {self.dirreccion}'
    
#pedido
class pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('preparacion', 'En preparación'),
        ('camino', 'En camino'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    ESTADOS_PAGO = [
        ('pendiente', 'Pendiente de pago'),
        ('pagado', 'Pagado')
    ]
    
    METODOS_PAGO = [
        ('efectivo', 'Efectivo (Contra entrega)'),
    ]
    
    TIPOS_ENTREGA = [
        ('express', ' Entrega Express (Hoy mismo)'),
        ('programada', ' Entrega Programada'),
    ]

    ZONAS_CALI = [
        ('norte', 'Zona Norte'),
        ('sur', 'Zona Sur'), 
        ('oriente', 'Zona Oriente'),
        ('occidente', 'Zona Occidente'),
        ('centro', 'Centro'),
    ]

    # Campos existentes
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    cliente = models.ForeignKey(cliente, on_delete=models.SET_NULL, null=True, blank=True)
    
    #SISTEMA DE ENTREGA INTELIGENTE
    tipo_entrega = models.CharField(max_length=20, choices=TIPOS_ENTREGA, default='express')
    zona_entrega = models.CharField(max_length=20, choices=ZONAS_CALI)
    fecha_entrega = models.DateField(null=True, blank=True)
    hora_entrega = models.TimeField(null=True, blank=True)
    
    # Información de entrega
    direccion_entrega = models.TextField(default="Por confirmar")
    ciudad = models.CharField(max_length=50, default='Cali')
    instrucciones_entrega = models.TextField(blank=True, null=True)
    
    # Sistema de pago
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='efectivo')
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='pendiente')
    
    # Sistema de seguimiento
    codigo_seguimiento = models.CharField(max_length=20, unique=True, blank=True, null=True)
    ubicacion_actual = models.CharField(max_length=100, default='Preparando pedido')
    
    # Auditoría
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    # Domiciliario asignado
    domiciliario = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'PEDIDO: #{self.id} - {self.cliente.nombre if self.cliente else "Cliente"} - ${self.total}'

    def save(self, *args, **kwargs):
        if not self.codigo_seguimiento:
            import uuid
            self.codigo_seguimiento = str(uuid.uuid4())[:8].upper()
            
        super().save(*args, **kwargs)

    
#detalle de cada producto en un pedido
class detallepedido(models.Model):
    pedido = models.ForeignKey(pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'PRODUCTO: {self.producto.nombre} x {self.cantidad} - {self.subtotal}'