import uuid
from django.db import models
from users.models import User
from carts.models import Cart

from django.db.models.signals import pre_save
from shipping_addresses.models import ShippingAddress
from .common import OrderStatus
from .common import choices
from billing_profiles.models import BillingProfile

class Order(models.Model):
    order_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    #usuario
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #carrito
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    #estado de la orden, las opcion son "OrderStatus"
    status = models.CharField(max_length=50, choices=choices, default=OrderStatus.CREATED)
    #ENVIO, LE PUSE POR DEFECTO 0
    shipping_total = models.DecimalField(default=0, max_digits=8 , decimal_places=2)
    #TOTAL, QUE ES LA SUMA DEL ENVIO + EL TOTAL DE CARRITO
    total = models.DecimalField(default=0, max_digits=8,decimal_places=2)
    shipping_address = models.ForeignKey(ShippingAddress, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True,on_delete=models.CASCADE)

    @property
    def description(self):
        return 'Compra por ({}) productos'.format(
            self.cart.products.count()
        )

    def __str__(self):
        return self.order_id

    def cancel(self):
        self.status = OrderStatus.CANCELED
        self.save()

    def complete(self):
        self.status = OrderStatus.COMPLETED
        self.save()

    def update_total(self):
        self.total = self.get_total()
        self.save()

    def update_shipping_address(self, shipping_address):
        self.shipping_address = shipping_address
        self.save()

    def get_total(self):
        return self.cart.total + self.shipping_total

    def get_or_set_billing_profile(self):
        if self.billing_profile:
            return self.billing_profile
        billing_profile = self.user.billing_profile
        if billing_profile:
            self.update_billing_profile(billing_profile)
        return billing_profile

    def update_billing_profile(self, billing_profile):
        self.billing_profile = billing_profile
        self.save()

    def get_or_set_shipping_address(self):
        #si la orden posee una direccion de envio
        #entonces return
        if self.shipping_address:
            return self.shipping_address

        shipping_address = self.user.shipping_address
        if shipping_address:
            self.update_shipping_address(shipping_address)
        return shipping_address

def set_order_id(sender,instance,*args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())

def set_total(sender, instance,*args, **kwargs):
    instance.total = instance.get_total()


pre_save.connect(set_order_id, sender=Order)
pre_save.connect(set_total, sender=Order)
##ANTES DE QUE OBJETO DE TIPO ORDER SE ALMACENE
## SE EJECUTA EL CALLBACK SET_TOTAL PAR ESTO ES
##PRE_SAVE
