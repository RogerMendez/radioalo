from django.urls import path

from . import views

urlpatterns = [
    path('conductor', views.conductor_index, name='conductor-index'),
    path('conductor/new', views.conductor_new, name='conductor-new'),
    path('conductor/<int:user_id>/update', views.conductor_update, name='conductor-update'),
    path('conductor/<int:user_id>/deactivate', views.conductor_deactivate, name='conductor-deactivate'),
    path('conductor/<int:user_id>/activate', views.conductor_activate, name='conductor-activate'),


    path('operador', views.operador_index, name='operador-index'),
    path('operador/new', views.operador_new, name='operador-new'),
    path('operador/<int:user_id>/update', views.operador_update, name='operador-update'),
    path('operador/<int:user_id>/deactivate', views.operador_deactivate, name='operador-deactivate'),
    path('operador/<int:user_id>/activate', views.operador_activate, name='operador-activate'),
]
