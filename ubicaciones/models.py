from django.db import models

from vehiculos.models import Vehiculo

class Ubicacion(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT)
    def __unicode__(self):
        return '%s: %s %s' % (self.vehiculo.placa, self.vehiculo.conductor.user.first_name, self.vehiculo.conductor.user.last_name)
    def __str__(self):
        return '%s: %s %s' % (
        self.vehiculo.placa, self.vehiculo.conductor.user.first_name, self.vehiculo.conductor.user.last_name)
    class Meta:
        verbose_name = 'Ubicacion'
        verbose_name_plural = 'Ubicaciones'
        ordering = ['fecha', 'hora']