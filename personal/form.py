from django import forms
from django.forms import ModelForm, TextInput

from personal.models import Conductor, Operador

class ConductorForm(ModelForm):
    class Meta:
        model = Conductor
        exclude = ['user']
        widgets = {
            'cedula': TextInput(attrs={'pattern': '[0-9]{6,7}', 'title': '0000000'})
        }

class OperadorForm(ModelForm):
    class Meta:
        model = Operador
        exclude = ['user']