from django.db import models

from personal.models import Conductor

SOAT = (
    ('SI', 'SI'),
    ('NO', 'NO'),
)

class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, verbose_name='Placa')
    marca = models.CharField(max_length=30, verbose_name='Marca Vehiculo')
    tipo = models.CharField(max_length=30, verbose_name='Tipo Vehiculo')
    color = models.CharField(max_length=10, verbose_name='Color Vehiculo')
    imagen = models.ImageField(upload_to='vehiculo', verbose_name='Imagen de Vehiculo')
    soat = models.CharField(max_length=100, default='SI', choices=SOAT, verbose_name='SOAT')
    nro_chasis = models.CharField(max_length=100, verbose_name='Numero de Chasis', default='')
    obs = models.TextField(verbose_name='Observaciones de Vehiculo')
    conductor = models.OneToOneField(Conductor, on_delete=models.PROTECT)
    def __unicode__(self):
        return '%s' % self.placa
    def __str__(self):
        return '%s' % self.placa
    class Meta:
        verbose_name = 'Vehiculo'
        verbose_name_plural = 'Vehiculos'
        ordering = ['conductor', 'placa']