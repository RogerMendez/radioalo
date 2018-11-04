from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, Http404, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, AdminPasswordChangeForm
from django.conf import settings
from django.utils.encoding import smart_str

from radioalo.general_utility import admin_log_addition, admin_log_change, render_pdf

from vehiculos.models import Vehiculo
from ubicaciones.models import Ubicacion
from pedidos.models import Pedido, PedidoVehiculo, Cliente

from reportes.form import FechaForm, EntreFechaForm, YearForm, MonthForm

import datetime

@login_required(login_url='/login')
def pedidos_fecha(request):
    fecha = datetime.datetime.now()
    form = FechaForm(request.GET or None)
    if form.is_valid():
        fecha = form.cleaned_data['fecha']
    #pedidos = Pedido.objects.filter(fecha=fecha)
    pedidovehiculos = PedidoVehiculo.objects.filter(
        pedido__fecha=fecha, pedido__estado=True, pedido__aceptado=True, pedido__rechazado=False, pedido__terminado=True
                                                    ).order_by('pedido__time', 'pedido__cliente')
    return render(request, 'reportes/pedido_fechas.html', {
        'form':form,
        'fecha':fecha,
        #'pedidos':pedidos,
        'pedidovehiculos':pedidovehiculos,
    })

@login_required(login_url='/login')
def pedidos_fecha_pdf(request, day, month, year):
    fecha = datetime.date(int(year), int(month), int(day))
    pedidovehiculos = PedidoVehiculo.objects.filter(
        pedido__fecha=fecha, pedido__estado=True, pedido__aceptado=True, pedido__rechazado=False, pedido__terminado=True
    ).order_by('pedido__time', 'pedido__cliente')
    html = render_to_string('reportes/pdf_pedido_fecha.html', {
        'fecha':fecha,
        'pedidovehiculos': pedidovehiculos,
    })
    return render_pdf(html, 'Reporte Pedido')

@login_required(login_url='/login')
def pedidos_entrefechas(request):
    inicio = fin = datetime.datetime.now()
    form = EntreFechaForm(request.GET or None)
    if form.is_valid():
        inicio = form.cleaned_data['inicio']
        fin = form.cleaned_data['fin']
    pedidovehiculos = PedidoVehiculo.objects.filter(
        pedido__fecha__gte=inicio, pedido__fecha__lte=fin, pedido__estado=True, pedido__aceptado=True, pedido__rechazado=False, pedido__terminado=True
    ).order_by('pedido__fecha', 'pedido__time', 'pedido__cliente')
    return render(request, 'reportes/pedido_entrefechas.html', {
        'form': form,
        'inicio': inicio,
        'fin':fin,
        'pedidovehiculos': pedidovehiculos,
    })

@login_required(login_url='/login')
def pdf_pedidos_entrefechas(request, day, month, year, day1, month1, year1):
    inicio = datetime.date(int(year), int(month), int(day))
    fin = datetime.date(int(year1), int(month1), int(day1))
    pedidovehiculos = PedidoVehiculo.objects.filter(
        pedido__fecha__gte=inicio, pedido__fecha__lte=fin, pedido__estado=True, pedido__aceptado=True, pedido__rechazado=False, pedido__terminado=True
    ).order_by('pedido__fecha', 'pedido__time', 'pedido__cliente')
    html = render_to_string('reportes/pdf_pedido_entrefechas.html', {
        'inicio': inicio,
        'fin':fin,
        'pedidovehiculos': pedidovehiculos,
    })
    return render_pdf(html)

@login_required(login_url='/login')
def list_vehiculos(request):
    vehiculos = Vehiculo.objects.filter(conductor__user__is_active=True)
    return render(request, 'reportes/list_vehiculos.html', {
        'vehiculos':vehiculos,
    })

@login_required(login_url='/login')
def pedidos_fecha_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk = vehiculo_id)
    inicio = fin = datetime.datetime.now()
    form = EntreFechaForm(request.GET or None)
    if form.is_valid():
        inicio = form.cleaned_data['inicio']
        fin = form.cleaned_data['fin']
    pedidovehiculos = PedidoVehiculo.objects.filter(
        pedido__fecha__gte=inicio, pedido__fecha__lte=fin, conductor=vehiculo.conductor, pedido__estado=True, pedido__aceptado=True, pedido__rechazado=False, pedido__terminado=True
    ).order_by(
            'pedido__fecha', 'pedido__time', 'pedido__cliente')
    return render(request, 'reportes/pedido_fechas_vehiculo.html', {
        'conductor':vehiculo.conductor,
        'form':form,
        'inicio': inicio,
        'fin':fin,
        'pedidovehiculos':pedidovehiculos,
    })

@login_required(login_url='/login')
def pdf_pedidos_vehiculo_entrefechas(request, vehiculo_id, day, month, year, day1, month1, year1):
    vehiculo = get_object_or_404(Vehiculo, pk = vehiculo_id)
    inicio = datetime.date(int(year), int(month), int(day))
    fin = datetime.date(int(year1), int(month1), int(day1))
    pedidovehiculos = PedidoVehiculo.objects.filter(
        pedido__fecha__gte=inicio, pedido__fecha__lte=fin, conductor__vehiculo=vehiculo, pedido__estado=True, pedido__aceptado=True, pedido__rechazado=False, pedido__terminado=True
    ).order_by('pedido__fecha', 'pedido__time', 'pedido__cliente')
    html = render_to_string('reportes/pdf_pedido_vehiculos_entrefechas.html', {
        'conductor':vehiculo.conductor,
        'inicio': inicio,
        'fin':fin,
        'pedidovehiculos': pedidovehiculos,
    })
    return render_pdf(html)

@login_required(login_url='/login')
def list_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'reportes/list_clientes.html', {
        'clientes':clientes,
    })

@login_required(login_url='/login')
def pedidos_fecha_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk = cliente_id)
    inicio = fin = datetime.datetime.now()
    form = EntreFechaForm(request.GET or None)
    if form.is_valid():
        inicio = form.cleaned_data['inicio']
        fin = form.cleaned_data['fin']
    pedidovehiculos = PedidoVehiculo.objects.filter(
        pedido__fecha__gte=inicio, pedido__fecha__lte=fin, pedido__cliente=cliente, pedido__estado=True, pedido__aceptado=True, pedido__rechazado=False, pedido__terminado=True
    ).order_by(
            'pedido__fecha', 'pedido__time', 'pedido__cliente')
    return render(request, 'reportes/pedido_fechas_cliente.html', {
        'cliente':cliente,
        'form':form,
        'inicio': inicio,
        'fin':fin,
        'pedidovehiculos':pedidovehiculos,
    })

@login_required(login_url='/login')
def pdf_pedidos_cliente_entrefechas(request, cliente_id, day, month, year, day1, month1, year1):
    cliente = get_object_or_404(Cliente, pk = cliente_id)
    inicio = datetime.date(int(year), int(month), int(day))
    fin = datetime.date(int(year1), int(month1), int(day1))
    pedidovehiculos = PedidoVehiculo.objects.filter(
        pedido__fecha__gte=inicio, pedido__fecha__lte=fin, pedido__cliente=cliente, pedido__estado=True, pedido__aceptado=True, pedido__rechazado=False, pedido__terminado=True
    ).order_by('pedido__fecha', 'pedido__time', 'pedido__cliente')
    html = render_to_string('reportes/pdf_pedido_cliente_entrefechas.html', {
        'cliente':cliente,
        'inicio': inicio,
        'fin':fin,
        'pedidovehiculos': pedidovehiculos,
    })
    return render_pdf(html)

@login_required(login_url='/login')
def pedidos_anuales(request):
    fecha = datetime.datetime.now()
    form = YearForm(request.GET or None)
    if form.is_valid():
        year = form.cleaned_data['year']
        fecha = datetime.date(int(year), 1, 1)
    pedidovehiculos = PedidoVehiculo.objects.filter(
        pedido__fecha__year=fecha.year,
        pedido__estado=True, pedido__aceptado=True, pedido__rechazado=False, pedido__terminado=True
    ).order_by('pedido__fecha', 'pedido__time', 'pedido__cliente')
    return render(request, 'reportes/pedido_anual.html', {
        'form': form,
        'fecha': fecha,
        # 'pedidos':pedidos,
        'pedidovehiculos': pedidovehiculos,
    })

@login_required(login_url='/login')
def pedidos_anual_pdf(request, year):
    fecha = datetime.date(int(year), 1, 1)
    pedidovehiculos = PedidoVehiculo.objects.filter(
        pedido__fecha__year=fecha.year,
        pedido__estado=True, pedido__aceptado=True, pedido__rechazado=False, pedido__terminado=True
    ).order_by('pedido__fecha', 'pedido__time', 'pedido__cliente')
    html = render_to_string('reportes/pdf_pedido_anual.html', {
        'fecha':fecha,
        'pedidovehiculos': pedidovehiculos,
    })
    return render_pdf(html, 'Reporte Pedido')

@login_required(login_url='/login')
def pedidos_mensuales(request):
    fecha = datetime.datetime.now()
    form = MonthForm(request.GET or None)
    if form.is_valid():
        year = form.cleaned_data['year']
        month = form.cleaned_data['month']
        fecha = datetime.date(int(year), int(month), 1)
    pedidovehiculos = PedidoVehiculo.objects.filter(
        pedido__fecha__year=fecha.year, pedido__fecha__month=fecha.month,
        pedido__estado=True, pedido__aceptado=True, pedido__rechazado=False, pedido__terminado=True
    ).order_by('pedido__fecha', 'pedido__time', 'pedido__cliente')
    return render(request, 'reportes/pedido_mensual.html', {
        'form': form,
        'fecha': fecha,
        # 'pedidos':pedidos,
        'pedidovehiculos': pedidovehiculos,
    })

@login_required(login_url='/login')
def pedidos_mensual_pdf(request, year, month):
    fecha = datetime.date(int(year), int(month), 1)
    pedidovehiculos = PedidoVehiculo.objects.filter(
        pedido__fecha__year=fecha.year, pedido__fecha__month=fecha.month,
        pedido__estado=True, pedido__aceptado=True, pedido__rechazado=False, pedido__terminado=True
    ).order_by('pedido__fecha', 'pedido__time', 'pedido__cliente')
    html = render_to_string('reportes/pdf_pedido_mensual.html', {
        'fecha':fecha,
        'pedidovehiculos': pedidovehiculos,
    })
    return render_pdf(html, 'Reporte Pedido')