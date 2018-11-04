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

from users.models import Perfil
from vehiculos.models import Vehiculo
from personal.models import Conductor
from pedidos.models import Cliente, Pedido, PedidoVehiculo
from movile.models import Seguimiento, Origen, Destino

from pedidos.form import ClienteForm, PedidoForm, VerifyPedido

@login_required(login_url='/login')
def list_moviles(request):
    perfils = Perfil.objects.filter(loget_in=True)
    conductores = Conductor.objects.filter(user_id__in=perfils.values('user_id'))
    #moviles = Vehiculo.objects.all()
    return render(request, 'pedidos/index.html', {
        #'moviles':moviles,
        'conductores':conductores,
    })

@login_required(login_url='/login')
def ajax_get_cliente(request):
    if request.is_ajax():
        cinit = request.GET['cinit']
        cliente = Cliente.objects.filter(cinit = cinit).values('razon', 'telefono', 'celular')
        return JsonResponse(list(cliente), safe=False)
    else:
        raise Http404

@login_required(login_url='/login')
def new_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        formpedido = PedidoForm(request.POST)
        if formpedido.is_valid() and form.is_valid():
            cinit = form.cleaned_data['cinit']
            if Cliente.objects.filter(cinit=cinit):
                cliente = Cliente.objects.get(cinit=cinit)
                cliente.razon = form.cleaned_data['razon']
                cliente.telefono = form.cleaned_data['telefono']
                cliente.celular = form.cleaned_data['celular']
                cliente.save()
                admin_log_change(request, cliente, 'Cliente Modificado')
            else:
                cliente = form.save()
                admin_log_addition(request, cliente, 'Cliente Registrado')
            pedido = formpedido.save(commit=False)
            pedido.cliente = cliente
            pedido.save()
            admin_log_addition(request, pedido, 'Pedido Regisrado')
            sms = 'Pedido Registrado Satisfactoriamente'
            messages.success(request, sms)
            return HttpResponseRedirect(reverse(new_list_moviles, args={pedido.id, }))
    else:
        form = ClienteForm()
        formpedido = PedidoForm()
    return render(request, 'pedidos/new_cliente.html', {
        'form': form,
        'formpedido':formpedido,
    })

@login_required(login_url='/login')
def new_list_moviles(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    perfils = Perfil.objects.filter(loget_in=True)
    aconductores = PedidoVehiculo.objects.filter(pedido=pedido)
    if pedido.cantidad > int(aconductores.count()):
        conductores = Conductor.objects.filter(user_id__in=perfils.values('user_id')).exclude(user_id__in=aconductores.values('conductor__user_id'))[0:10]
    else:
        conductores = ''
    print(conductores)
    return render(request, 'pedidos/new_list_moviles.html', {
        'pedido':pedido,
        'conductores': conductores,
        'aconductores': aconductores,
    })

@login_required(login_url='/login')
def conductor_vehiculo(request, pedido_id, conductor_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    conductor = get_object_or_404(Conductor, pk = conductor_id)
    pedidovehiculo = PedidoVehiculo.objects.create(
        pedido = pedido,
        conductor = conductor,
    )
    pedidovehiculo.save()
    admin_log_addition(request, pedidovehiculo, 'Conductor Asignado')
    messages.success(request, 'Movil Asignado Correctamente a Pedido')
    return HttpResponseRedirect(reverse(new_list_moviles, args={pedido.id, }))

@login_required(login_url='/login')
def delete_vehiculo(request, cvehiculo_id):
    cvehiculo = get_object_or_404(PedidoVehiculo, pk = cvehiculo_id)
    cvehiculo.delete()
    messages.error(request, 'Vehiculo Quitado Correctamente', 'danger')
    return HttpResponseRedirect(reverse(new_list_moviles, args={cvehiculo.pedido.id, }))

@login_required(login_url='/login')
def confirm_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    pedido.estado = True
    pedido.save()
    messages.success(request, 'Pedido Confirmado Correctamente')
    messages.warning(request, 'Pëdido Enviado a Movil(es)')
    messages.error(request, 'Puede Verficar la ubicacion de su movil con el Codigo Nro,: %s' %pedido.id, 'danger')
    return HttpResponseRedirect(reverse(new_cliente))

@login_required(login_url='/login')
def pedidos_confirmados(request):
    pedidos = Pedido.objects.filter(estado=True, aceptado=False, rechazado=False, terminado=False)
    return render(request, 'pedidos/confirmados.html', {
        'pedidos':pedidos,
    })

@login_required(login_url='/login')
def pedidos_aceptados(request):
    pedidos = Pedido.objects.filter(estado=True, aceptado=True, rechazado=False, terminado=False).order_by('fecha', 'time')
    return render(request, 'pedidos/aceptados.html', {
        'pedidos':pedidos,
    })

@login_required(login_url='/login')
def seguimiento_pedido(request, pedido_id, conductor_id):
    pedido = get_object_or_404(Pedido, pk = pedido_id)
    conductor = get_object_or_404(Conductor, pk = conductor_id)
    return render(request, 'pedidos/seguimiento_pedido.html', {
        'pedido':pedido,
        'conductor':conductor,
    })

def ajax_position_actual(request, pedido_id, conductor_id):
    if request.is_ajax():
        pedido = get_object_or_404(Pedido, pk = pedido_id)
        conductor = get_object_or_404(Conductor, pk = conductor_id)
        seguimientos = Seguimiento.objects.filter(pedido=pedido, conductor=conductor).order_by('-fecha', '-hora')
        posiciones = seguimientos.values('latitud', 'longitud')
        print('Posision Actual de movil')
        return JsonResponse(list(posiciones), safe=False)
    else:
        raise Http404

@login_required(login_url='/login')
def pedidos_rechazados(request):
    pedidos = Pedido.objects.filter(estado=True, aceptado=False, rechazado=True, terminado=False).order_by('fecha', 'time')
    return render(request, 'pedidos/rechazados.html', {
        'pedidos':pedidos,
    })

@login_required(login_url='/login')
def pedidos_terminados(request):
    pedidos = Pedido.objects.filter(estado=True, aceptado=True, rechazado=False, terminado=True).order_by('-fecha', '-time')
    return render(request, 'pedidos/terminados.html', {
        'pedidos':pedidos,
    })

@login_required(login_url='/login')
def pedido_terminado(request, pedido_id, conductor_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    conductor = get_object_or_404(Conductor, pk=conductor_id)
    origenes = Origen.objects.filter(pedido=pedido, conductor=conductor)
    destinos = Destino.objects.filter(pedido=pedido, conductor=conductor)
    seguimientos = Seguimiento.objects.filter(pedido=pedido, conductor=conductor).order_by('fecha', 'hora')[0:10]
    return render(request, 'pedidos/pedido_terminado.html', {
        'pedido':pedido,
        'conductor':conductor,
        'origenes':origenes,
        'destinos': destinos,
        'seguimientos':seguimientos,
    })

def verifi_pedido(request):
    pedido = None
    if request.method == 'POST':
        form = VerifyPedido(request.POST)
        #if form.is_valid():
        id = request.POST['codigo']
        if Pedido.objects.filter(id = id):
            pedido = Pedido.objects.get(id = id)
    else:
        form = VerifyPedido()
    return render(request, 'pedidos/verify_pedido.html', {
        'form':form,
        'pedido':pedido,
    })

@login_required(login_url='/login')
def index_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/index.html', {
        'clientes':clientes,
    })

@login_required(login_url='/login')
def register_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            admin_log_addition(request, cliente, 'Cliente Registrado')
            messages.success(request, 'Cliente %s Registrado Correctamente' % cliente.razon)
            return HttpResponseRedirect(reverse(index_clientes))
    else:
        form = ClienteForm()
    return render(request, 'clientes/new.html', {
        'form':form
    })

@login_required(login_url='/login')
def update_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk = cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            admin_log_change(request, cliente, 'Cliente Modificado')
            messages.warning(request, 'Cliente %s Modificado Correctamete')
            return HttpResponseRedirect(reverse(index_clientes))
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/update.html', {
        'form':form,
    })

@login_required(login_url='/login')
def activate_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk = cliente_id)
    cliente.estado = True
    cliente.save()
    admin_log_change(request, cliente, 'Cliente Activado')
    messages.success(request, 'Cliente %s Activado' % cliente.razon)
    return HttpResponseRedirect(reverse(index_clientes))

@login_required(login_url='/login')
def deactivate_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk = cliente_id)
    cliente.estado = False
    cliente.save()
    admin_log_change(request, cliente, 'Cliente Desactivado')
    messages.error(request, 'Cliente %s Desactivado' % cliente.razon, 'danger')
    return HttpResponseRedirect(reverse(index_clientes))