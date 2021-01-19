from django.contrib import admin
from .models import Product
# Register your models here.

#ESTO ES PARA ADMINISTRAR DESDE EL ADMINITRADOR DE DJANGO
class ProductAdmin(admin.ModelAdmin):
    #CAMPOS QUE QUEREMOS QUE SE MUESTREN A LA HORA DE AGREGAR PRODUCTO EN EL ADMIN.
    fields = ('title', 'description' , 'price' , 'image')
    #CAMPOS QUE QUEREMOS QUE SE MUESTREN A LA HORA DE CONSULTAR EN EL ADMIN.
    list_display = ('__str__' , 'slug' , 'created_at')

#ESTO ES NECESARIO PARA QUE PRODUCTOS APARESCA EN ADMIN
admin.site.register(Product, ProductAdmin)
