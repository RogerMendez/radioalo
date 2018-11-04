from django import template

register = template.Library()

from django.shortcuts import get_object_or_404

from ubicaciones.models import Ubicacion
from personal.models import Conductor
from vehiculos.models import Vehiculo

import datetime

@register.simple_tag
def ubicacion_moviles(vehiculo_id):
    hoy = datetime.datetime.now()
    vehiculo = get_object_or_404(Vehiculo, pk = vehiculo_id)
    ubicacion = Ubicacion.objects.filter(vehiculo=vehiculo, fecha__day=hoy.day, fecha__month=hoy.month, fecha__year=hoy.year).order_by('fecha', 'hora')
    return ubicacion.last()