from django.db import models

from personal.models import Conductor

class Cliente(models.Model):
    cinit = models.CharField(max_length=10, verbose_name='CI/NIT')
    razon =  models.CharField(max_length=100, verbose_name='Razon/Nombres')
    telefono = models.IntegerField(verbose_name='Telefono', null=True, blank=True)
    celular = models.IntegerField(verbose_name='Celular', null=True, blank=True)
    estado = models.BooleanField(default=True)
    def __unicode__(self):
        return '%s' %self.razon
    def __str__(self):
        return '%s' % self.razon
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['cinit']

class Pedido(models.Model):
    fecha = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    cantidad = models.IntegerField(verbose_name='Cantidad de Moviles')
    direccion = models.TextField(verbose_name='Direccion de Origen')
    monto = models.FloatField(verbose_name='Costo de Pedido', default=0)
    estado = models.BooleanField(default=False)#si el pedido es aceptado por el operador
    aceptado = models.BooleanField(default=False)#si el pedido es aceptado por el vehiculo
    rechazado = models.BooleanField(default=False)#si el pedido es rechazado por el vehiculo
    terminado = models.BooleanField(default=False)#si el pedido ya termino
    olat = models.FloatField(null=True)
    olong = models.FloatField(null=True)
    dlat = models.FloatField(null=True)
    dlong = models.FloatField(null=True)
    def __str__(self):
        return '%s %s' % (self.fecha, self.cliente)
    def __unicode__(self):
        return '%s %s' % (self.fecha, self.cliente)
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['cliente', 'fecha']

class PedidoVehiculo(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT)
