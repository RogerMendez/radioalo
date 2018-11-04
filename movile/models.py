from django.db import models

from pedidos.models import Pedido
from personal.models import Conductor

class Origen(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT, null=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    def __str__(self):
        return '%s - %s' % (self.fecha, self.pedido)
    def __unicode__(self):
        return '%s - %s' % (self.fecha, self.pedido)
    class Meta:
        verbose_name = '_Ubicacion de Origen'
        verbose_name_plural = '_Ubicaciones de Origen'
        ordering = ['pedido', 'fecha', 'hora']

class Destino(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT, null=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    def __str__(self):
        return '%s - %s' % (self.fecha, self.pedido)
    def __unicode__(self):
        return '%s - %s' % (self.fecha, self.pedido)
    class Meta:
        verbose_name = '_Ubicacion de Destino'
        verbose_name_plural = '_Ubicaciones de Destino'
        ordering = ['pedido', 'fecha', 'hora']

class Seguimiento(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    conductor = models.ForeignKey(Conductor, on_delete=models.PROTECT, null=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    def __str__(self):
        return '%s - %s' % (self.fecha, self.pedido)
    def __unicode__(self):
        return '%s - %s' % (self.fecha, self.pedido)
    class Meta:
        verbose_name = '_Seguimiento de Pedido'
        verbose_name_plural = '_Seguimientos de Pedido'
        ordering = ['pedido', 'fecha', 'hora']