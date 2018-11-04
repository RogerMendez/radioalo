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

from users.models import Perfil
from personal.models import Conductor
from vehiculos.models import Vehiculo
from users.form import UserForm, UsernameForm, PerfilForm

def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(user_index))
    return render(request, 'home.html')

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse(user_index))
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            access = authenticate(username=username, password=password)
            if access is not None:
                if access.is_active:
                    login(request, access)
                    user = request.user
                    if user.first_name:
                        perfil = user.perfil
                        perfil.loget_in = True
                        perfil.save()
                    if 'next' in request.GET:
                        msm = "Inicio de Sesion Correcto <strong>Gracias Por Su Visita</strong>"
                        messages.add_message(request, messages.INFO, msm)
                        return HttpResponseRedirect(str(request.GET['next']))
                    else:
                        msm = "Inicio de Sesion Existoso <strong>Gracias Por Su Visita</strong>"
                        messages.add_message(request, messages.SUCCESS, msm)
                        return HttpResponseRedirect(reverse(user_index))
                else:
                    sms = "Su Cuenta No Esta Activada <strong>Contactese con el Administrador</strong>"
                    messages.warning(request, sms)
                    return HttpResponseRedirect('/')
            else:
                msm = "Usted No Es Usuario Del Sistema"
                messages.add_message(request, messages.ERROR, msm, 'danger')
                return HttpResponseRedirect(reverse(user_login))
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {
        'form':form,
    })

@login_required(login_url='/login')
def user_index(request):
    if Conductor.objects.filter(user=request.user):
        conductor = Conductor.objects.get(user=request.user)
        from pedidos.models import Pedido, PedidoVehiculo
        from movile.views import movile_seguimiento
        pedidos = PedidoVehiculo.objects.filter(conductor=conductor, pedido__estado=True, pedido__aceptado=True,
                                                pedido__rechazado=False, pedido__terminado=False)
        if pedidos:
            return HttpResponseRedirect(reverse(movile_seguimiento, args={pedidos.first().pedido.id, }))
        vehiculos = Vehiculo.objects.filter(conductor__user=request.user)
        return render(request, 'movile/index.html', {
            'vehiculos':vehiculos,
        })
    return render(request, 'users/index.html')

@login_required(login_url='/login/')
def user_logout(request):
    user = request.user
    if user.first_name:
        perfil = user.perfil
        perfil.loget_in = False
        perfil.save()
    logout(request)
    sms = 'Gracias Por Su Visita'
    messages.info(request, sms)
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def reset_pass(request):
    if request.method == 'POST' :
        form = AdminPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(user_index))
    else:
        form = AdminPasswordChangeForm(user=request.user)
    return  render(request,'users/reset_pass.html', {
        'form' :form,
        })

@login_required(login_url='/login/')
def change_username(request):
    if request.method == 'POST' :
        form = UsernameForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            sms = 'Nombre De Usuario Modificado Correctamente'
            messages.info(request, sms)
            return HttpResponseRedirect(reverse(user_index))
    else:
        form= UsernameForm(instance=request.user)
    return  render(request, 'users/change_username.html', {
        'form' :form,
    })

@login_required(login_url='/login/')
def complete_information(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        formperfil = PerfilForm(request.POST)
        if form.is_valid() and formperfil.is_valid():
            user = form.save()
            perfil = formperfil.save(commit=False)
            perfil.user = user
            perfil.save()
            admin_log_change(request, user, 'Datos Completados')
            admin_log_addition(request, perfil, 'Perfil creado')
            messages.info(request, 'Perfil Completado Correctamente')
            return HttpResponseRedirect(reverse(user_index))
    else:
        form = UserForm(instance=request.user)
        formperfil = PerfilForm()
    return render(request, 'users/complete_information.html', {
        'form':form,
        'formperfil':formperfil,
    })

@login_required(login_url='/login/')
def update_information(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        formperfil = PerfilForm(request.POST, instance=request.user.perfil)
        if form.is_valid() and formperfil.is_valid():
            user = form.save()
            perfil = formperfil.save(commit=False)
            perfil.user = user
            perfil.save()
            admin_log_change(request, user, 'Datos modificados')
            admin_log_addition(request, perfil, 'Perfil modificado')
            messages.info(request, 'Perfil Modificado Correctamente')
            return HttpResponseRedirect(reverse(user_index))
    else:
        form = UserForm(instance=request.user)
        formperfil = PerfilForm(instance=request.user.perfil)
    return render(request, 'users/complete_information.html', {
        'form':form,
        'formperfil':formperfil,
    })

@permission_required('users.add_user', login_url='/login/')
def new_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            u = form.save()
            admin_log_addition(request, u, 'Usuario Registrado')
            perfil = Perfil.objects.create(
                hotel=request.user.perfil.hotel,
                user=u,
            )
            perfil.save()
            admin_log_addition(request, perfil, 'Perfil Creado')
            sms = 'Usuario %s Registrado Correctamente'%u.username
            messages.success(request, sms)
            return HttpResponseRedirect(reverse(user_index))
    else:
        form = UserCreationForm()
    return render(request, 'users/new.html', {
        'form':form,
    })