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
from ubicaciones.models import Ubicacion

@login_required(login_url='/login')
def save_ubicacion(request):
    if request.is_ajax():
        vehiculo = request.user.conductor.vehiculo
        latitud = request.GET['latitud']
        longitud = request.GET['longitud']
        ubicacion = Ubicacion.objects.create(
            longitud=longitud,
            latitud=latitud,
            vehiculo=vehiculo,
        )
        ubicacion.save()
        print('Ubicacion Enviada')
        admin_log_addition(request, ubicacion, 'Ubicacion Guardadas')
        return JsonResponse('si', safe=False)
    else:
        raise Http404