import django_filters

from .models import *

class ProductoFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ('genero' , 'forma' , 'color', 'marca' , 'material' , 'talla')

class ProductoFilter2(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ('uso', 'tipo', 'marcacontacto')
