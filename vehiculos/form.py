from django import forms
from django.forms import ModelForm, TextInput

from vehiculos.models import Vehiculo

class VehiculoForm(ModelForm):
    class Meta:
        model = Vehiculo
        exclude = ['conductor']
        widgets = {
            'placa': TextInput(attrs={'pattern': '[0-9]{3,4}[A-Z]{3}', 'title': '0000XXX'})
        }