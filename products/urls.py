from django.urls import path
from . import views

#con este comando le estamos diciendo que todas estas rutas
#pertenecen a esta app


app_name = 'products'

urlpatterns = [
    #search TIENE QUE IR PRIMERO, SI O SI, PARA QUE EL SEARCH FUNCIONE CORRECTAMENTE.
    path('search', views.ProductSearchListView.as_view(), name='search'),
    path('<slug:slug>', views.ProductDetalView.as_view(), name='product'), #id llave primaria
]
