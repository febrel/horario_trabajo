from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
     path('logout/', views.logout_page, name='logout'),
    path('registrar/', views.registro, name='registrar'),
    path('productos/', views.productos, name='productos'),
    path('usuarios/', views.usuarios, name='usuarios'),
]