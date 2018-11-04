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

from django.contrib.auth.models import User
from users.models import Perfil
from personal.models import Conductor, Operador

from personal.form import ConductorForm, OperadorForm
from users.form import PerfilForm, UserForm

@login_required(login_url='/login')
def conductor_index(request):
    conductores = Conductor.objects.all()
    return render(request, 'conductores/index.html', {
        'conductores':conductores,
    })

@permission_required('personal.add_conductor', login_url='/login')
def conductor_new(request):
    if request.method == 'POST':
        form = ConductorForm(request.POST)
        formperfil = PerfilForm(request.POST)
        formuser = UserForm(request.POST)
        if form.is_valid() and formperfil.is_valid() and formuser.is_valid():
            cedula = form.cleaned_data['cedula']
            email = formuser.cleaned_data['email']
            user = User.objects.create_user(str(cedula), email, str(cedula))
            user.first_name = formuser.cleaned_data['first_name']
            user.last_name = formuser.cleaned_data['last_name']
            user.save()
            perfil = formperfil.save(commit=False)
            perfil.user = user
            perfil.save()
            conductor = form.save(commit=False)
            conductor.user = user
            conductor.save()
            messages.success(request, 'Conductor Registrado Correctamente')
            admin_log_addition(request, perfil, 'Perfil Conductor Registrado')
            admin_log_addition(request, conductor, 'Conductor Registrado')
            return HttpResponseRedirect(reverse(conductor_index))
    else:
        form = ConductorForm()
        formperfil = PerfilForm()
        formuser = UserForm()
    return render(request, 'conductores/new.html', {
        'formperfil':formperfil,
        'formuser':formuser,
        'form':form,
    })

@permission_required('personal.add_conductor', login_url='/login')
def conductor_update(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    perfil = Perfil.objects.get(user=user)
    conductor = Conductor.objects.get(user=user)
    if request.method == 'POST':
        form = ConductorForm(request.POST, instance=conductor)
        formperfil = PerfilForm(request.POST, instance=perfil)
        formuser = UserForm(request.POST, instance=user)
        if form.is_valid() and formperfil.is_valid() and formuser.is_valid():
            formuser.save()
            perfil = formperfil.save()
            conductor = form.save()
            messages.warning(request, 'Conductor Modificado Correctamente')
            admin_log_change(request, perfil, 'Perfil Conductor Modificado')
            admin_log_change(request, conductor, 'Conductor Modificado')
            return HttpResponseRedirect(reverse(conductor_index))
    else:
        form = ConductorForm(instance=conductor)
        formperfil = PerfilForm(instance=perfil)
        formuser = UserForm(instance=user)
    return render(request, 'conductores/update.html', {
        'formperfil':formperfil,
        'formuser':formuser,
        'form':form,
    })

@permission_required('personal.deactivate_conductor', login_url='/login')
def conductor_deactivate(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    user.is_active = False
    user.save()
    messages.warning(request, 'Conductor Desactivado')
    return HttpResponseRedirect(reverse(conductor_index))

@permission_required('personal.activate_conductor', login_url='/login')
def conductor_activate(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    user.is_active = True
    user.save()
    messages.success(request, 'Conductor Activado')
    return HttpResponseRedirect(reverse(conductor_index))

@login_required(login_url='/login')
def operador_index(request):
    operadores = Operador.objects.all()
    return render(request, 'operadores/index.html', {
        'operadores':operadores,
    })

@permission_required('personal.add_operador', login_url='/login')
def operador_new(request):
    if request.method == 'POST':
        form = OperadorForm(request.POST)
        formperfil = PerfilForm(request.POST)
        formuser = UserForm(request.POST)
        if form.is_valid() and formperfil.is_valid() and formuser.is_valid():
            cedula = form.cleaned_data['cedula']
            email = formuser.cleaned_data['email']
            user = User.objects.create_user(str(cedula), email, str(cedula))
            user.first_name = formuser.cleaned_data['first_name']
            user.last_name = formuser.cleaned_data['last_name']
            user.save()
            perfil = formperfil.save(commit=False)
            perfil.user = user
            perfil.save()
            operador = form.save(commit=False)
            operador.user = user
            operador.save()
            messages.success(request, 'Operador Registrado Correctamente')
            admin_log_addition(request, perfil, 'Perfil Conductor Registrado')
            admin_log_addition(request, operador, 'Operador Registrado')
            return HttpResponseRedirect(reverse(operador_index))
    else:
        form = OperadorForm()
        formperfil = PerfilForm()
        formuser = UserForm()
    return render(request, 'operadores/new.html', {
        'formperfil':formperfil,
        'formuser':formuser,
        'form':form,
    })

@permission_required('personal.add_conductor', login_url='/login')
def operador_update(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    perfil = Perfil.objects.get(user=user)
    operador = Operador.objects.get(user=user)
    if request.method == 'POST':
        form = OperadorForm(request.POST, instance=operador)
        formperfil = PerfilForm(request.POST, instance=perfil)
        formuser = UserForm(request.POST, instance=user)
        if form.is_valid() and formperfil.is_valid() and formuser.is_valid():
            formuser.save()
            perfil = formperfil.save()
            conductor = form.save()
            messages.warning(request, 'Operador Modificado Correctamente')
            admin_log_change(request, perfil, 'Perfil Conductor Modificado')
            admin_log_change(request, conductor, 'Conductor Modificado')
            return HttpResponseRedirect(reverse(operador_index))
    else:
        form = OperadorForm(instance=operador)
        formperfil = PerfilForm(instance=perfil)
        formuser = UserForm(instance=user)
    return render(request, 'operadores/update.html', {
        'formperfil':formperfil,
        'formuser':formuser,
        'form':form,
    })

@permission_required('personal.deactivate_operador', login_url='/login')
def operador_deactivate(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    user.is_active = False
    user.save()
    messages.warning(request, 'Operador Desactivado')
    return HttpResponseRedirect(reverse(operador_index))

@permission_required('personal.activate_operador', login_url='/login')
def operador_activate(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    user.is_active = True
    user.save()
    messages.success(request, 'Operador Activado')
    return HttpResponseRedirect(reverse(operador_index))