from django.urls import path

from . import views


urlpatterns = [
    path('save', views.save_ubicacion, name='ubicacion-save'),
]
