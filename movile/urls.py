from django.urls import path

from . import views


urlpatterns = [
    path('pedido/<int:pedido_id>/cancel', views.rechazar_pedido, name='movile-pedido-cancel'),
    path('pedido/<int:pedido_id>/accept', views.aceptar_pedido, name='movile-pedido-accept'),
    path('pedido/<int:pedido_id>/seguimiento/accept', views.movile_seguimiento, name='movile-pedido-seguimiento'),

    path('pedido/register/<int:pedido_id>/<int:conductor_id>/origen', views.register_origen, name='movile-pedido-register-origen'),
    path('pedido/register/<int:pedido_id>/<int:conductor_id>/destino', views.register_destino, name='movile-pedido-register-destino'),
    path('pedido/terminate/<int:pedido_id>/register', views.terminate_pedido, name='movile-pedido-terminate'),

    path('ajax/pedidos', views.ajax_pedidos, name='movile-ajax-pedido'),
    path('ajax/<int:pedido_id>/<int:conductor_id>/save/seguimiento', views.ajax_save_seguimiento, name='movile-ajax-pedido-seguimiento'),
]
