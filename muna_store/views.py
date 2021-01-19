
from django.shortcuts import render
from django.shortcuts import redirect

#MENSAJE DEL SERVIDOR AL CLIENTE.
from django.contrib import messages

#PARA AUTENTICAR.
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
#from django.contrib.auth.models import User
from users.models import User
from .forms import RegisterForm
from products.models import Product
from django.http import HttpResponseRedirect


def index(request):
    products = Product.objects.all().order_by('-id')

    return render(request, 'index.html' , {
        'message': 'Listado de productos',
        'title': 'Productos',
        'products' : products,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])
            return redirect('index')
        else:
            messages.error(request, 'Usuario/contraseña no valido')

    return render(request, 'users/login.html' , {})


def logout_view(request):
    logout(request)
    messages.success(request, 'Sesiòn cerrada exitosamente')
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')



    #acceder a la info del formulario.
    #SI LA PETICION ES CON EL METODO POST, CREA UN formulario
    #CON LA INFO QUE EL USUARIO PUSO EN EL.
    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        #creamos el usuario, el metodo create_user se encarga de encriptar el password
        #que esta en el forms.py
        user = form.save()
        if user:
            login(request,user)
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('index')

    return render(request, 'users/register.html', {
        'form': form
    })
