from django import forms
from django.forms import ModelForm, TextInput, HiddenInput

from pedidos.models import Cliente, Pedido

import datetime

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        exclude = ['cliente', 'terminado', 'aceptado', 'rechazado', 'estado', 'monto']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        exclude = ['estado']

class VerifyPedido(forms.Form):
    codigo = forms.IntegerField(label='Codigo Asignado')