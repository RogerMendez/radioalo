from django.db import models

from django.contrib.auth.models import User

class Perfil(models.Model):
    direccion = models.CharField(max_length=100, verbose_name='Direccion', null=True)
    celular = models.IntegerField(verbose_name='Celular', null=True, blank=True)
    #avatar = m/odels.ImageField(upload_to='avatar', verbose_name='Seleccione foto perfil')
    loget_in = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    def __unicode__(self):
        return '%s' % self.user.first_name
    def __str__(self):
        return '%s' % self.user.first_name
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        ordering = ['user']