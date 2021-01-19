from django.shortcuts import render
from .models import Cart
# Create your views here.
from .utils import get_or_create_cart

from products.models import Product
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import CartProducts
def cart(request):
    #CREAR UNA Session
    #request.session['cart_id'] = '123'
    #OBtendremos el valor de una session
    #valor = request.session.get('cart_id')
    #Eliminar una sessions
    #request.session['cart_id'] = None

    #obtenemos el usuario authenticate caso contrario, none

    cart = get_or_create_cart(request)

    return render(request, 'carts/cart.html', {
        'cart': cart
    })

def add(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity', 1))

    #cart.products.add(product, through_defaults={
    #    'quantity': quantity
    #})
    cart_product = CartProducts.objects.create_or_update_quantity(
                                                                cart=cart,
                                                                product=product,
                                                                quantity=quantity)

    return render(request, 'carts/add.html', {
        'quantity': quantity,
        'cart_product' : cart_product,
        'product': product
    })

def remove(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))

    cart.products.remove(product)

    return redirect('carts:cart')
