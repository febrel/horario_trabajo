from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Registro
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Para registro
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from datetime import datetime, timedelta
import time
import threading




# Create your views here.
@login_required
def home(request):

    # Guardo la fecha actual del sistema
    now = datetime.now()
    entrada = now.strftime('%d-%m-%Y')


    # Query DB
    registros_obtenidos = Registro.objects.all()
    filtro_registros = registros_obtenidos.filter(usuario=request.user)
    filtro_contador = registros_obtenidos.filter(usuario=request.user).count()

    # Solo muestra los ultimos 2
    filtro_ultimo = filtro_registros.order_by('-fecha_creado')[:2]
   
   
    dato = filtro_registros.order_by('fecha_creado').last()

    contador = filtro_contador

    fecha_db = dato.fecha_creado.strftime('%d-%m-%Y')

    # Comprueba que no tenga registros del ultimo dia
    if entrada != fecha_db:
        contador = 0
 

    # Si recibe un post
    if request.method == 'POST':
        hora_recibida = request.POST.get('timepkr')
        
        # Para ingresar el estado
        if contador <= 0:
            estado_creado = 'Entrada'
        else:
            estado_creado = 'Salida'
    

        # Guarda en la DB
        registro = Registro(usuario=request.user, hora_actual=hora_recibida, estado=estado_creado)
        registro.save()
    


    contexto = {'registros':filtro_ultimo,'filtro':contador}

    return render(request, 'cuentas/dashboard.html', contexto)


def login_page(request):

    if request.method == 'POST':
        # Captura los datos de inputs por POST
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        valida_usuario = authenticate(request, username=username, password=password)

        if valida_usuario is not None:
            login(request, valida_usuario)
            return redirect('home')
        else:
            messages.error(request, 'Los datos no son correctos!')
            return redirect('login')

    contexto = {}

    return render(request, 'cuentas/login.html', contexto)



def logout_page(request):
    logout(request)

    return redirect('login')


def registro(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # Captura los datos de inputs por POST
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Controla qe passwod tenga mas de 3
        if len(password) <= 3:
            messages.error(request, 'Password debe tener mas de 3 caracteres!')
            return redirect('registrar')

        # Controla que no se utilice el mismo usuario
        mismo_username = User.objects.filter(username=username)

        if mismo_username:
            messages.error(request, 'El usuario ingresado ya existe!')
            return redirect('registrar')

        # Registra usuario nuevo
        usuario_nuevo = User.objects.create_user(username=username, email=email, password=password)
        usuario_nuevo.save()

        messages.success(request, 'Usuario creado con exito!')
        return redirect('login')

    contexto = {}
    return render(request, 'cuentas/registrar.html', contexto)


def productos(request):

    return render(request, 'cuentas/lista_productos.html')


def usuarios(request):

    return render(request, 'cuentas/usuarios.html')