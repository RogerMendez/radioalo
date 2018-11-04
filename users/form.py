from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
from users.models import Perfil

class UsernameForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        exclude = ['user', 'hotel', 'loget_in']