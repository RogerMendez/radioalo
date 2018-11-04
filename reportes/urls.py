from django.urls import path

from . import views


urlpatterns = [
    path('pedido/fechas', views.pedidos_fecha, name='report-fecha'),
    path('pedido/entre/fechas', views.pedidos_entrefechas, name='report--entre-fecha'),

    path('pedido/list/vehiculo', views.list_vehiculos, name='report-list-vehiculos'),
    path('pedido/vehiculo/<int:vehiculo_id>/fechas', views.pedidos_fecha_vehiculo, name='report-vehiculo-fecha'),

    path('pedido/list/cliente', views.list_clientes, name='report-list-clientes'),
    path('pedido/cliente/<int:cliente_id>/fechas', views.pedidos_fecha_cliente, name='report-cliente-fecha'),

    path('pedido/anual', views.pedidos_anuales, name='report-pedido-anual'),
    path('pedido/mensual', views.pedidos_mensuales, name='report-pedido-mensual'),

    path('pdf/pedido/<int:day>/<int:month>/<int:year>/fechas', views.pedidos_fecha_pdf, name='report-fecha-pdf'),
    path('pdf/pedido/entre/fechas/<int:day>/<int:month>/<int:year>/<int:day1>/<int:month1>/<int:year1>/fechas',
         views.pdf_pedidos_entrefechas, name='report-entre-fecha-pdf'),

    path('pdf/pedido/vehiculo/entre/fechas/<int:vehiculo_id>/<int:day>/<int:month>/<int:year>/<int:day1>/<int:month1>/<int:year1>/fechas',
         views.pdf_pedidos_vehiculo_entrefechas, name='report-vehiculo-entre-fecha-pdf'),

    path('pdf/pedido/cliente/entre/fechas/<int:cliente_id>/<int:day>/<int:month>/<int:year>/<int:day1>/<int:month1>/<int:year1>/fechas',
         views.pdf_pedidos_cliente_entrefechas, name='report-cliente-entre-fecha-pdf'),

    path('pdf/pedido/anual/<int:year>', views.pedidos_anual_pdf, name='report-pedido-anual-pdf'),
    path('pdf/pedido/mensual/<int:year>/<int:month>', views.pedidos_mensual_pdf, name='report-pedido-mensual-pdf'),

]
