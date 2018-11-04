from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.user_login, name='user-login'),
    path('logout', views.user_logout, name='user-logout'),
    path('user/index', views.user_index, name='user-index'),
    path('change/pass/', views.reset_pass, name='user-reset-pass'),
    path('change/username/', views.change_username, name='user-change-username'),
    path('complete/information/', views.complete_information, name='user-complete-information'),
    path('update/information/', views.update_information, name='user-update-information'),
]
