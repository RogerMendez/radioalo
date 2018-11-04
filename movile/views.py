from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.encoding import smart_str

from radioalo.general_utility import admin_log_addition, admin_log_change

from movile.models import Origen, Seguimiento, Destino
from users.models import Perfil
from personal.models import Conductor
from pedidos.models import Pedido, PedidoVehiculo

@login_required(login_url='/login')
def ajax_pedidos(request):
    if request.is_ajax():
        #html = request.GET['html']
        user = request.user
        conductor = Conductor.objects.get(user=user)
        pedidos = PedidoVehiculo.objects.filter(conductor=conductor, pedido__estado=True, pedido__aceptado=False, pedido__rechazado=False, pedido__terminado=False)
        html = render_to_string('movile/__pedido.html', {
            'pedido':pedidos.first(),
            'conductor':conductor,
        })
        return JsonResponse(html, safe=False)
    else:
        raise Http404

@login_required(login_url='/login')
def aceptar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    pedido.aceptado = True
    user = request.user
    conductor = Conductor.objects.get(user=user)
    origen = Origen.objects.create(
        pedido=pedido,
        latitud=request.GET['latitud'],
        longitud=request.GET['longitud'],
        conductor=conductor
    )
    origen.save()
    pedido.save()
    messages.success(request, 'Pedido Aceptado Satisfactoriamente')
    return HttpResponseRedirect(reverse(movile_seguimiento, args={pedido.id, }))

@login_required(login_url='/login')
def rechazar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    pedido.rechazado = True
    pedido.save()
    messages.error(request, 'Pedido Rechazado', 'danger')
    return HttpResponseRedirect('/login')

@login_required(login_url='/login')
def movile_seguimiento(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    user = request.user
    conductor = Conductor.objects.get(user=user)
    pedidos = PedidoVehiculo.objects.filter(conductor=conductor, pedido__estado=True, pedido__aceptado=True,
                                            pedido__rechazado=False, pedido__terminado=False, pedido=pedido)
    return render(request, 'movile/seguimiento.html', {
        'pedidos':pedidos,
        'pedido':pedido,
        'conductor':conductor,
    })

@login_required(login_url='/login')
def ajax_save_seguimiento(request, pedido_id, conductor_id):
    if request.is_ajax():
        conductor =get_object_or_404(Conductor, pk = conductor_id)
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        seguimiento = Seguimiento.objects.create(
            pedido=pedido,
            latitud=request.GET['latitud'],
            longitud=request.GET['longitud'],
            conductor=conductor
        )
        seguimiento.save()
        return JsonResponse('si', safe=False)
    else:
        raise Http404

@login_required(login_url='/login')
def register_origen(request, pedido_id, conductor_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    conductor = get_object_or_404(Conductor, pk = conductor_id)
    origen = Origen.objects.create(
        pedido=pedido,
        latitud=request.GET['latitud'],
        longitud=request.GET['longitud'],
        conductor=conductor
    )
    origen.save()
    admin_log_addition(request, origen, 'Destino Registrado')
    messages.success(request, 'Origen Registrado Correctamente')
    return HttpResponseRedirect(reverse(movile_seguimiento, args={pedido.id, }))

@login_required(login_url='/login')
def register_destino(request, pedido_id, conductor_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    conductor = get_object_or_404(Conductor, pk = conductor_id)
    destino = Destino.objects.create(
        pedido=pedido,
        latitud=request.GET['latitud'],
        longitud=request.GET['longitud'],
        conductor=conductor
    )
    destino.save()
    admin_log_addition(request, destino, 'Destino Registrado')
    messages.success(request, 'Destino Registrado Correctamente')
    return HttpResponseRedirect(reverse(movile_seguimiento, args={pedido.id, }))

@login_required(login_url='/login')
def terminate_pedido(request, pedido_id):
    if request.method == 'POST':
        monto = request.POST['monto']
        pedido = get_object_or_404(Pedido, pk = pedido_id)
        pedido.terminado = True
        pedido.monto = monto
        pedido.save()
        admin_log_addition(request, pedido, 'Pedido Terminado')
        messages.warning(request, 'Pedido Terminado Satisfactoriamente')
        return HttpResponseRedirect('/login')
    else:
        messages.error(request, 'Ocurrio un Error', 'danger')
        messages.info(request, 'Vuelva a Registrar el Monto del Pedido')
        return HttpResponseRedirect(reverse(movile_seguimiento, args={pedido_id, }))