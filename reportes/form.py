from django import forms
from django.forms import ModelForm, TextInput

from personal.models import Conductor, Operador
import datetime

class FechaForm(forms.Form):
    fecha = forms.DateField(label='Seleccione Una Fecha',
                            widget=forms.TextInput(attrs={'type': 'date', 'required': 'required'}))
    def clean_fecha(self):
        today = datetime.datetime.now()
        data = self.cleaned_data['fecha']
        if data.strftime('%Y-%m-%d') > today.strftime('%Y-%m-%d'):
            raise forms.ValidationError('No Puede Seleccionar Una Fecha Mayor a la Actual')
        return data

class EntreFechaForm(forms.Form):
    inicio = forms.DateField(label='Fecha de Inicio',
                            widget=forms.TextInput(attrs={'type': 'date', 'required': 'required'}))
    fin = forms.DateField(label='Fecha de Finalizacion',
                             widget=forms.TextInput(attrs={'type': 'date', 'required': 'required'}))

class YearForm(forms.Form):
    hoy = datetime.datetime.now()
    anho = hoy.strftime("%Y")
    a_ini = int(anho) - 10
    a_fin = int(anho) + 1
    anhos = ()
    for a in range(a_ini, a_fin):
        anhos += ((a, a),)
    year = forms.ChoiceField(choices=anhos, label=u'Seleccione Año')

class MonthForm(forms.Form):
    hoy = datetime.datetime.now()
    anho = hoy.strftime("%Y")
    a_ini = int(anho) - 10
    a_fin = int(anho) + 1
    anhos = ()
    for a in range(a_ini, a_fin):
        anhos += ((a, a),)
    year = forms.ChoiceField(choices=anhos, label=u'Seleccione Año')
    meses = (
        ('01','Enero'),
        ('02','Febrero'),
        ('03','Marzo'),
        ('04','Abril'),
        ('05','Mayo'),
        ('06','Junio'),
        ('07','Julio'),
        ('08','Agosto'),
        ('09','Septiembre'),
        ('10','Octubre'),
        ('11','Noviembre'),
        ('12','Diciembre'),
    )
    month = forms.ChoiceField(choices=meses, label="Seleccione un Mes")