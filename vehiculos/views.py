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

from radioalo.general_utility import admin_log_addition, admin_log_change

from vehiculos.models import Vehiculo
from personal.models import Conductor
from vehiculos.form import VehiculoForm

@login_required(login_url='/login')
def index(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculos/index.html', {
        'vehiculos':vehiculos,
    })

@permission_required('vehiculos.add_vehiculo', login_url='/login')
def new(request, conductor_id):
    conductor = get_object_or_404(Conductor, pk = conductor_id)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.conductor = conductor
            vehiculo.save()
            messages.success(request, 'Vehiculo Registrado Correctamente')
            admin_log_addition(request, vehiculo, 'Vehiculo Registrado')
            return HttpResponseRedirect(reverse(index))
    else:
        form = VehiculoForm()
    return render(request, 'vehiculos/new.html', {
        'form':form,
        'conductor':conductor,
    })

@permission_required('vehiculos.change_vehiculo', login_url='/login')
def update(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk = vehiculo_id)
    conductor = Conductor.objects.get(id = vehiculo.conductor.id)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES, instance=vehiculo)
        if form.is_valid():
            vehiculo = form.save()
            messages.success(request, 'Vehiculo Registrado Correctamente')
            admin_log_addition(request, vehiculo, 'Vehiculo Registrado')
            return HttpResponseRedirect(reverse(index))
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'vehiculos/update.html', {
        'form':form,
        'conductor':conductor,
    })