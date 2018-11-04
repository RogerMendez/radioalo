from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='vehiculo-index'),
    path('<int:conductor_id>/new', views.new, name='vehiculo-new'),
    path('<int:vehiculo_id>/update', views.update, name='vehiculo-update'),

]
