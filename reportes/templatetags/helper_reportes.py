from django import template
register = template.Library()

from django.db.models import Sum

from pedidos.models import Pedido

@register.simple_tag
def monto_total(pedidovehiculos):
    costo = 0
    if pedidovehiculos:
        sumservicios = pedidovehiculos.aggregate(Sum('pedido__monto'))
        costo = sumservicios['pedido__monto__sum']
    return costo

@register.simple_tag
def pedidos_cliente(cliente):
    pedidos = Pedido.objects.filter(cliente=cliente)
    return pedidos.__len__()