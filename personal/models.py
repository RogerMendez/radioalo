from django.db import models

from django.contrib.auth.models import User

CATEGORIA = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
)
SOAT = (
    ('SI', 'SI'),
    ('NO', 'NO'),
)

class Conductor(models.Model):
    cedula = models.CharField(max_length=20, verbose_name='Cedula de Identidad', unique=True)
    phone = models.IntegerField(verbose_name='Telefono de Referencia')
    ciudad = models.CharField(max_length=20, verbose_name='Ciudad de Origen')
    nro_licencia = models.CharField(max_length=20, verbose_name='Numero de Licencia')
    categoria = models.CharField(max_length=10, verbose_name='Categoria Licencia', choices=CATEGORIA)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    def __unicode__(self):
        return '%s: %s %s' % (self.cedula, self.user.first_name, self.user.last_name)
    def __str__(self):
        return '%s: %s %s' % (self.cedula, self.user.first_name, self.user.last_name)
    class Meta:
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'
        ordering = ['cedula']
        permissions = (
            ('activate_conductor', 'Activar Conductor'),
            ('deactivate_conductor', 'Desactivar Conductor'),
        )

class Operador(models.Model):
    cedula = models.IntegerField(verbose_name='Cedula de Identidad', unique=True)
    phone = models.IntegerField(verbose_name='Telefono de Referencia')
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    def __unicode__(self):
        return '%s: %s %s' % (self.cedula, self.user.first_name, self.user.last_name)
    def __str__(self):
        return '%s: %s %s' % (self.cedula, self.user.first_name, self.user.last_name)
    class Meta:
        verbose_name = 'Operador'
        verbose_name_plural = 'Operadores'
        ordering = ['cedula']
        permissions = (
            ('activate_operador', 'Activar Operador'),
            ('deactivate_operador', 'Desactivar Operador'),
        )