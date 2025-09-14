from django.db import models

#fecha: 12SEP2025 se crean modelos para la tienda.

#categorias (cervezas comerciales, cervezas artesanales, vinos comerciales, vinos artesanales, licores).
class categoria (models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

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

    def __str__(self):
        return f'NOMBRE: {self.nombre} - PRECIO: {self.precio} - CANTIDA DISPONIBLE: {self.stock}'
    
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
        ('pendiente', 'pendiente'),
        ('pagado', 'pagado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
    ]

    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    tracking_ling = models.URLField(blank=True, null=True)
    cliente = models.ForeignKey(cliente, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'PEDIDO: #{self.id} - ESTADO: {self.estado} - FECHA: {self.fecha} - CLIENTE: {self.cliente}'
    
#detalle de cada producto en un pedido
class detallepedido(models.Model):
    pedido = models.ForeignKey(pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'PRODUCTO: {self.producto.nombre} x {self.cantidad} - {self.subtotal}'