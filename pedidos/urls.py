from django.urls import path

from . import views


urlpatterns = [
    path('', views.list_moviles, name='pedidos-list_conductores'),
    path('cliente/new', views.new_cliente, name='pedidos-new-cliente'),
    path('<int:pedido_id>/list/moviles', views.new_list_moviles, name='pedidos-new-list-clientes'),
    path('asignacion/<int:pedido_id>/<int:conductor_id>/pedido/vehiculo', views.conductor_vehiculo, name='pedidos-new-conductor-vehiculo'),
    path('asignacion/<int:cvehiculo_id>/delete/vehiculo', views.delete_vehiculo, name='pedidos-new-delete-vehiculo-pedido'),
    path('confirm/<int:pedido_id>/vehiculo', views.confirm_pedido, name='pedidos-confirm-vehiculo'),
    path('confirms', views.pedidos_confirmados, name='pedidos-confirmados'),
    path('accepts', views.pedidos_aceptados, name='pedidos-aceptados'),
    path('tracing/<int:pedido_id>/<int:conductor_id>', views.seguimiento_pedido, name='pedidos-seguimiento'),

    path('rejected', views.pedidos_rechazados, name='pedidos-rechazados'),
    path('finished', views.pedidos_terminados, name='pedidos-terminados'),
    path('finished/<int:pedido_id>/<int:conductor_id>/view', views.pedido_terminado, name='pedidos-terminado-show'),


    path('ajax/cliente/getting', views.ajax_get_cliente, name='pedidos-ajax-cliente-getting'),
    path('ajax/<int:pedido_id>/<int:conductor_id>/position/actual', views.ajax_position_actual, name='pedidos-ajax-position-actual'),

    path('verify', views.verifi_pedido, name='pedidos-verify'),


    #CLIENTES
    path('clientes', views.index_clientes, name='clientes-index'),
    path('cliente/register', views.register_cliente, name='clientes-new'),
    path('cliente/update/<int:cliente_id>', views.update_cliente, name='cliente-update'),
    path('cliente/activate/<int:cliente_id>', views.activate_cliente, name='cliente-activate'),
    path('cliente/deactivate/<int:cliente_id>', views.deactivate_cliente, name='cliente-deactivate'),

]
