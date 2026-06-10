from django.http import Http404
from django.utils.text import slugify

from django.db.models import Count, Q

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
import datetime 
from django.core.paginator import Paginator
from .models import * 
from .utils import cookieCart, cartData

from .filters import ProductoFilter, ProductoFilter2 



from django.http import HttpResponse 
from django.views.decorators.csrf import csrf_exempt
import os
import requests


def home(request):
    products = Producto.objects.filter(nuevo=1)
    myFilter = ProductoFilter(request.GET, queryset=products)
    Lproducts=myFilter.qs
    paginator=Paginator(Lproducts,24)
    pagina=request.GET.get("page") or 1
    products=paginator.get_page(pagina)
    pagina_actual=int(pagina)
    paginas=range(1, products.paginator.num_pages + 1)
    
    context = {'products':products, 'paginas':paginas,'pagina_actual': pagina_actual, 'myFilter': myFilter}
    return render(request, 'store/home.html', context)


def lentes_oftalmicos(request):
    return _render_lentes_oftalmicos(request)


def lentes_de_sol(request):
    return _render_lentes_de_sol(request)


def lentes_de_contacto(request):
    return _render_lentes_de_contacto(request)

def uso_lentes_de_contacto(request,uso_id):
	products = Producto.objects.filter(clase=3).filter(uso_id=uso_id).filter(cantidad__gte=1)
	myFilter = ProductoFilter(request.GET, queryset=products)
	Lproducts=myFilter.qs
	paginator=Paginator(Lproducts,24)
	pagina=request.GET.get("page") or 1
	products=paginator.get_page(pagina)
	pagina_actual=int(pagina)
	paginas=range(1, products.paginator.num_pages + 1)

	
	context = {'products':products, 'paginas':paginas,'pagina_actual': pagina_actual, 'myFilter': myFilter}
	return render(request, 'store/uso_lentes_de_contacto.html', context)


def tipo_lentes_de_contacto(request,tipo_id):
	products = Producto.objects.filter(clase=3).filter(tipo_id=tipo_id).filter(cantidad__gte=1)
	myFilter = ProductoFilter(request.GET, queryset=products)
	Lproducts=myFilter.qs
	paginator=Paginator(Lproducts,24)
	pagina=request.GET.get("page") or 1
	products=paginator.get_page(pagina)
	pagina_actual=int(pagina)
	paginas=range(1, products.paginator.num_pages + 1)

	
	context = {'products':products, 'paginas':paginas,'pagina_actual': pagina_actual, 'myFilter': myFilter}
	return render(request, 'store/tipo_lentes_de_contacto.html', context)


def single(request, id):
    product = get_object_or_404(Producto, id=id)
    context = {'product': product}
    return render(request, 'store/single.html', context)

def legal(request):
	context = {}
	return render(request, 'store/legal.html', context)	



def nosotros(request):
	context = {}
	return render(request, 'store/nosotros.html', context)


#CEO
def producto_detalle(request, slug):
    product = get_object_or_404(
        Producto,
        slug=slug,
        activo=True
    )

    productos_relacionados = Producto.objects.filter(
        tipo=product.tipo,
        activo=True,
        stock__gte=1
    ).exclude(pk=product.pk)[:8]

    context = {
        'product': product,
        'productos_relacionados': productos_relacionados,
    }
    return render(request, 'store/single.html', context)



def _render_lentes_oftalmicos(request, filtros_iniciales=None):
    filtros_iniciales = filtros_iniciales or {}
    categoria = filtros_iniciales.get('categoria', request.GET.get('categoria', '').strip())
    marca = filtros_iniciales.get('marca', request.GET.get('marca', '').strip())
    talla = filtros_iniciales.get('talla', request.GET.get('talla', '').strip())
    forma = filtros_iniciales.get('forma', request.GET.get('forma', '').strip())
    material = filtros_iniciales.get('material', request.GET.get('material', '').strip())
    color = filtros_iniciales.get('color', request.GET.get('color', '').strip())
    precio = filtros_iniciales.get('precio', request.GET.get('precio', '').strip())

    base_products = Producto.objects.filter(
        tipo="Monturas oftálmicas",
        stock__gte=1,
        activo=True
    ).order_by('-precio_venta')

    def aplicar_filtros(qs, exclude_field=None):
        if categoria and exclude_field != 'categoria':
            qs = qs.filter(categoria__iexact=categoria)

        if marca and exclude_field != 'marca':
            qs = qs.filter(marca__iexact=marca)

        if talla and exclude_field != 'talla':
            qs = qs.filter(talla__iexact=talla)

        if forma and exclude_field != 'forma':
            qs = qs.filter(forma__iexact=forma)

        if material and exclude_field != 'material':
            qs = qs.filter(material__iexact=material)

        if color and exclude_field != 'color':
            qs = qs.filter(color__iexact=color)

        if precio and exclude_field != 'precio':
            if precio == '0-100':
                qs = qs.filter(precio_venta__gte=0, precio_venta__lte=100)
            elif precio == '101-200':
                qs = qs.filter(precio_venta__gte=101, precio_venta__lte=200)
            elif precio == '201-300':
                qs = qs.filter(precio_venta__gte=201, precio_venta__lte=300)
            elif precio == '301-500':
                qs = qs.filter(precio_venta__gte=301, precio_venta__lte=500)
            elif precio == '500+':
                qs = qs.filter(precio_venta__gt=500)
        return qs

    def obtener_opciones_campo(nombre_campo):
        qs = aplicar_filtros(base_products, exclude_field=nombre_campo)
        qs = qs.exclude(**{nombre_campo: ""}).filter(**{f"{nombre_campo}__isnull": False})

        opciones = (
            qs.values(nombre_campo)
            .annotate(total=Count('pk'))
            .order_by(nombre_campo)
        )

        return [
            {'valor': item[nombre_campo], 'total': item['total']}
            for item in opciones if item[nombre_campo]
        ]

    def obtener_opciones_precio():
        qs = aplicar_filtros(base_products, exclude_field='precio')

        rangos = [
            {'valor': '0-100', 'label': 'Hasta S/100', 'filtro': Q(precio_venta__gte=0, precio_venta__lte=100)},
            {'valor': '101-200', 'label': 'S/101 a S/200', 'filtro': Q(precio_venta__gte=101, precio_venta__lte=200)},
            {'valor': '201-300', 'label': 'S/201 a S/300', 'filtro': Q(precio_venta__gte=201, precio_venta__lte=300)},
            {'valor': '301-500', 'label': 'S/301 a S/500', 'filtro': Q(precio_venta__gte=301, precio_venta__lte=500)},
            {'valor': '500+', 'label': 'Más de S/500', 'filtro': Q(precio_venta__gt=500)},
        ]

        resultado = []
        for rango in rangos:
            total = qs.filter(rango['filtro']).count()
            if total > 0:
                resultado.append({
                    'valor': rango['valor'],
                    'label': rango['label'],
                    'total': total,
                })
        return resultado

    products_qs = aplicar_filtros(base_products)

    paginator = Paginator(products_qs, 24)
    pagina = request.GET.get("page") or 1
    products = paginator.get_page(pagina)

    try:
        pagina_actual = int(pagina)
    except ValueError:
        pagina_actual = 1

    paginas = range(1, products.paginator.num_pages + 1)

    marcas_opciones = obtener_opciones_campo('marca')
    categorias_opciones = obtener_opciones_campo('categoria')
    tallas_opciones = obtener_opciones_campo('talla')
    formas_opciones = obtener_opciones_campo('forma')
    materiales_opciones = obtener_opciones_campo('material')
    colores_opciones = obtener_opciones_campo('color')
    precios_opciones = obtener_opciones_precio()

    filtros_activos = []

    if categoria:
        filtros_activos.append({'tipo': 'categoria', 'label': categoria})
    if marca:
        filtros_activos.append({'tipo': 'marca', 'label': marca})
    if talla:
        filtros_activos.append({'tipo': 'talla', 'label': talla})
    if forma:
        filtros_activos.append({'tipo': 'forma', 'label': forma})
    if material:
        filtros_activos.append({'tipo': 'material', 'label': material})
    if color:
        filtros_activos.append({'tipo': 'color', 'label': color})
    if precio:
        mapa_precios = {
            '0-100': 'Hasta S/100',
            '101-200': 'S/101 a S/200',
            '201-300': 'S/201 a S/300',
            '301-500': 'S/301 a S/500',
            '500+': 'Más de S/500',
        }
        filtros_activos.append({'tipo': 'precio', 'label': mapa_precios.get(precio, precio)})

    context = {
        'products': products,
        'paginas': paginas,
        'pagina_actual': pagina_actual,

        'categoria_actual': categoria,
        'marca_actual': marca,
        'talla_actual': talla,
        'forma_actual': forma,
        'material_actual': material,
        'color_actual': color,
        'precio_actual': precio,

        'marcas_opciones': marcas_opciones,
        'categorias_opciones': categorias_opciones,
        'tallas_opciones': tallas_opciones,
        'formas_opciones': formas_opciones,
        'materiales_opciones': materiales_opciones,
        'colores_opciones': colores_opciones,
        'precios_opciones': precios_opciones,

        'filtros_activos': filtros_activos,
    }

    return render(request, 'store/lentes_oftalmicos.html', context)


def lentes_categoria(request, valor):
    mapa_categoria = {
        'hombre': 'Hombre',
        'mujer': 'Mujer',
        'nino': 'Nino',
    }

    categoria_real = mapa_categoria.get(valor.lower())
    if not categoria_real:
        raise Http404("Género no encontrado")

    return _render_lentes_oftalmicos(request, filtros_iniciales={
        'categoria': categoria_real
    })

def lentes_forma(request, valor):
    mapa_forma = {
        'agatado': 'Agatado',
        'almendra': 'Almendra',
        'piloto': 'Piloto',
        'cuadrado': 'Cuadrado',
        'redondo': 'Redondo',
        'exagonal': 'Exagonal',
        'otros': 'Otros',
    }

    forma_real = mapa_forma.get(valor.lower())
    if not forma_real:
        raise Http404("Forma no encontrada")

    return _render_lentes_oftalmicos(request, filtros_iniciales={
        'forma': forma_real
    })    




def lentes_marca(request, valor):
    mapa_marca = {
        'ray-ban': 'Ray-Ban',
        'nike': 'Nike',
        'oakley': 'Oakley',
        'guess': 'Guess',
        'tommy-hilfiger': 'Tommy-Hilfiger',
        'arnette': 'Arnette',
        'nano': 'Nano',
        'razza': 'Razza',
        'otros': 'Otros',
    }

    marca_real = mapa_marca.get(valor.lower())
    if not marca_real:
        raise Http404("Marca no encontrada")

    return _render_lentes_oftalmicos(request, filtros_iniciales={
        'marca': marca_real
    })

def lentes_talla(request, valor):
    mapa_talla = {
        'grande': 'Grande',
        'mediana': 'Mediana',
        'chica': 'Chica',
    }

    talla_real = mapa_talla.get(valor.lower())
    if not talla_real:
        raise Http404("Talla no encontrada")

    return _render_lentes_oftalmicos(request, filtros_iniciales={
        'talla': talla_real
    })






#................GAFAS.................

def _render_lentes_de_sol(request, filtros_iniciales=None):
    filtros_iniciales = filtros_iniciales or {}
    categoria = filtros_iniciales.get('categoria', request.GET.get('categoria', '').strip())
    marca = filtros_iniciales.get('marca', request.GET.get('marca', '').strip())
    talla = filtros_iniciales.get('talla', request.GET.get('talla', '').strip())
    forma = filtros_iniciales.get('forma', request.GET.get('forma', '').strip())
    material = filtros_iniciales.get('material', request.GET.get('material', '').strip())
    color = filtros_iniciales.get('color', request.GET.get('color', '').strip())
    precio = filtros_iniciales.get('precio', request.GET.get('precio', '').strip())

    base_products = Producto.objects.filter(
        tipo="Monturas Solares",
        stock__gte=1,
        activo=True
    ).order_by('-precio_venta')

    def aplicar_filtros(qs, exclude_field=None):
        if categoria and exclude_field != 'categoria':
            qs = qs.filter(categoria__iexact=categoria)

        if marca and exclude_field != 'marca':
            qs = qs.filter(marca__iexact=marca)

        if talla and exclude_field != 'talla':
            qs = qs.filter(talla__iexact=talla)

        if forma and exclude_field != 'forma':
            qs = qs.filter(forma__iexact=forma)

        if material and exclude_field != 'material':
            qs = qs.filter(material__iexact=material)

        if color and exclude_field != 'color':
            qs = qs.filter(color__iexact=color)

        if precio and exclude_field != 'precio':
            if precio == '0-100':
                qs = qs.filter(precio_venta__gte=0, precio_venta__lte=100)
            elif precio == '101-200':
                qs = qs.filter(precio_venta__gte=101, precio_venta__lte=200)
            elif precio == '201-300':
                qs = qs.filter(precio_venta__gte=201, precio_venta__lte=300)
            elif precio == '301-500':
                qs = qs.filter(precio_venta__gte=301, precio_venta__lte=500)
            elif precio == '500+':
                qs = qs.filter(precio_venta__gt=500)
        return qs

    def obtener_opciones_campo(nombre_campo):
        qs = aplicar_filtros(base_products, exclude_field=nombre_campo)
        qs = qs.exclude(**{nombre_campo: ""}).filter(**{f"{nombre_campo}__isnull": False})

        opciones = (
            qs.values(nombre_campo)
            .annotate(total=Count('pk'))
            .order_by(nombre_campo)
        )

        return [
            {'valor': item[nombre_campo], 'total': item['total']}
            for item in opciones if item[nombre_campo]
        ]

    def obtener_opciones_precio():
        qs = aplicar_filtros(base_products, exclude_field='precio')

        rangos = [
            {'valor': '0-100', 'label': 'Hasta S/100', 'filtro': Q(precio_venta__gte=0, precio_venta__lte=100)},
            {'valor': '101-200', 'label': 'S/101 a S/200', 'filtro': Q(precio_venta__gte=101, precio_venta__lte=200)},
            {'valor': '201-300', 'label': 'S/201 a S/300', 'filtro': Q(precio_venta__gte=201, precio_venta__lte=300)},
            {'valor': '301-500', 'label': 'S/301 a S/500', 'filtro': Q(precio_venta__gte=301, precio_venta__lte=500)},
            {'valor': '500+', 'label': 'Más de S/500', 'filtro': Q(precio_venta__gt=500)},
        ]

        resultado = []
        for rango in rangos:
            total = qs.filter(rango['filtro']).count()
            if total > 0:
                resultado.append({
                    'valor': rango['valor'],
                    'label': rango['label'],
                    'total': total,
                })
        return resultado

    products_qs = aplicar_filtros(base_products)

    paginator = Paginator(products_qs, 24)
    pagina = request.GET.get("page") or 1
    products = paginator.get_page(pagina)

    try:
        pagina_actual = int(pagina)
    except ValueError:
        pagina_actual = 1

    paginas = range(1, products.paginator.num_pages + 1)

    marcas_opciones = obtener_opciones_campo('marca')
    categorias_opciones = obtener_opciones_campo('categoria')
    tallas_opciones = obtener_opciones_campo('talla')
    formas_opciones = obtener_opciones_campo('forma')
    materiales_opciones = obtener_opciones_campo('material')
    colores_opciones = obtener_opciones_campo('color')
    precios_opciones = obtener_opciones_precio()

    filtros_activos = []

    if categoria:
        filtros_activos.append({'tipo': 'categoria', 'label': categoria})
    if marca:
        filtros_activos.append({'tipo': 'marca', 'label': marca})
    if talla:
        filtros_activos.append({'tipo': 'talla', 'label': talla})
    if forma:
        filtros_activos.append({'tipo': 'forma', 'label': forma})
    if material:
        filtros_activos.append({'tipo': 'material', 'label': material})
    if color:
        filtros_activos.append({'tipo': 'color', 'label': color})
    if precio:
        mapa_precios = {
            '0-100': 'Hasta S/100',
            '101-200': 'S/101 a S/200',
            '201-300': 'S/201 a S/300',
            '301-500': 'S/301 a S/500',
            '500+': 'Más de S/500',
        }
        filtros_activos.append({'tipo': 'precio', 'label': mapa_precios.get(precio, precio)})

    context = {
        'products': products,
        'paginas': paginas,
        'pagina_actual': pagina_actual,

        'categoria_actual': categoria,
        'marca_actual': marca,
        'talla_actual': talla,
        'forma_actual': forma,
        'material_actual': material,
        'color_actual': color,
        'precio_actual': precio,

        'marcas_opciones': marcas_opciones,
        'categorias_opciones': categorias_opciones,
        'tallas_opciones': tallas_opciones,
        'formas_opciones': formas_opciones,
        'materiales_opciones': materiales_opciones,
        'colores_opciones': colores_opciones,
        'precios_opciones': precios_opciones,

        'filtros_activos': filtros_activos,
    }

    return render(request, 'store/lentes_de_sol.html', context)

def gafas_genero(request, valor):
    mapa_genero = {
        'hombre': 'Hombre',
        'mujer': 'Mujer',
        'nino': 'Nino',
    }

    genero_real = mapa_genero.get(valor.lower())
    if not genero_real:
        raise Http404("Género no encontrado")

    return _render_lentes_de_sol(request, filtros_iniciales={
        'categoria': genero_real
    })

def gafas_forma(request, valor):
    mapa_forma = {
        'agatado': 'Agatado',
        'almendra': 'Almendra',
        'piloto': 'Piloto',
        'cuadrado': 'Cuadrado',
        'redondo': 'Redondo',
        'exagonal': 'Exagonal',
        'otros': 'Otros',
    }

    forma_real = mapa_forma.get(valor.lower())
    if not forma_real:
        raise Http404("Forma no encontrada")

    return _render_lentes_de_sol(request, filtros_iniciales={
        'forma': forma_real
    })    




def gafas_marca(request, valor):
    mapa_marca = {
        'ray-ban': 'Ray-Ban',
        'nike': 'Nike',
        'oakley': 'Oakley',
        'guess': 'Guess',
        'tommy-hilfiger': 'Tommy-Hilfiger',
        'arnette': 'Arnette',
        'nano': 'Nano',
        'razza': 'Razza',
        'otros': 'Otros',
    }

    marca_real = mapa_marca.get(valor.lower())
    if not marca_real:
        raise Http404("Marca no encontrada")

    return _render_lentes_de_sol(request, filtros_iniciales={
        'marca': marca_real
    })

def gafas_talla(request, valor):
    mapa_talla = {
        'grande': 'Grande',
        'mediana': 'Mediana',
        'chica': 'Chica',
    }

    talla_real = mapa_talla.get(valor.lower())
    if not talla_real:
        raise Http404("Talla no encontrada")

    return _render_lentes_de_sol(request, filtros_iniciales={
        'talla': talla_real
    })


#-------------------Lentes de Contacto-----------------------

def _render_lentes_de_contacto(request, filtros_iniciales=None):
    filtros_iniciales = filtros_iniciales or {}

    marca = filtros_iniciales.get('marca', request.GET.get('marca', '').strip())
    uso = filtros_iniciales.get('uso', request.GET.get('uso', '').strip())
    condicion = filtros_iniciales.get('condicion', request.GET.get('condicion', '').strip())
    precio = filtros_iniciales.get('precio', request.GET.get('precio', '').strip())

    base_products = Producto.objects.filter(
        tipo="Lentes de Contacto",
        stock__gte=0,
        activo=True
    ).order_by('-precio_venta')

    def aplicar_filtros(qs, exclude_field=None):
        if marca and exclude_field != 'marca':
            qs = qs.filter(marca__iexact=marca)

        if uso and exclude_field != 'uso':
            qs = qs.filter(uso__iexact=uso)

        if condicion and exclude_field != 'condicion':
            qs = qs.filter(condicion__iexact=condicion)

        if precio and exclude_field != 'precio':
            if precio == '0-100':
                qs = qs.filter(precio_venta__gte=0, precio_venta__lte=100)
            elif precio == '101-200':
                qs = qs.filter(precio_venta__gte=101, precio_venta__lte=200)
            elif precio == '201-300':
                qs = qs.filter(precio_venta__gte=201, precio_venta__lte=300)
            elif precio == '301-500':
                qs = qs.filter(precio_venta__gte=301, precio_venta__lte=500)
            elif precio == '500+':
                qs = qs.filter(precio_venta__gt=500)
        return qs

    def obtener_opciones_campo(nombre_campo):
        qs = aplicar_filtros(base_products, exclude_field=nombre_campo)
        qs = qs.exclude(**{nombre_campo: ""}).filter(**{f"{nombre_campo}__isnull": False})

        opciones = (
            qs.values(nombre_campo)
            .annotate(total=Count('pk'))
            .order_by(nombre_campo)
        )

        return [
            {'valor': item[nombre_campo], 'total': item['total']}
            for item in opciones if item[nombre_campo]
        ]

    def obtener_opciones_precio():
        qs = aplicar_filtros(base_products, exclude_field='precio')

        rangos = [
            {'valor': '0-100', 'label': 'Hasta S/100', 'filtro': Q(precio_venta__gte=0, precio_venta__lte=100)},
            {'valor': '101-200', 'label': 'S/101 a S/200', 'filtro': Q(precio_venta__gte=101, precio_venta__lte=200)},
            {'valor': '201-300', 'label': 'S/201 a S/300', 'filtro': Q(precio_venta__gte=201, precio_venta__lte=300)},
            {'valor': '301-500', 'label': 'S/301 a S/500', 'filtro': Q(precio_venta__gte=301, precio_venta__lte=500)},
            {'valor': '500+', 'label': 'Más de S/500', 'filtro': Q(precio_venta__gt=500)},
        ]

        resultado = []
        for rango in rangos:
            total = qs.filter(rango['filtro']).count()
            if total > 0:
                resultado.append({
                    'valor': rango['valor'],
                    'label': rango['label'],
                    'total': total,
                })
        return resultado

    products_qs = aplicar_filtros(base_products)

    paginator = Paginator(products_qs, 24)
    pagina = request.GET.get("page") or 1
    products = paginator.get_page(pagina)

    try:
        pagina_actual = int(pagina)
    except ValueError:
        pagina_actual = 1

    paginas = range(1, products.paginator.num_pages + 1)

    marcas_opciones = obtener_opciones_campo('marca')
    uso_opciones = obtener_opciones_campo('uso')
    condicion_opciones = obtener_opciones_campo('condicion')
    precios_opciones = obtener_opciones_precio()
    filtros_activos = []

    if marca:
        filtros_activos.append({'tipo': 'marca', 'label': marca})
    if uso:
        filtros_activos.append({'tipo': 'uso', 'label': uso})
    if condicion:
        filtros_activos.append({'tipo': 'condicion', 'label': condicion})
    if precio:
        mapa_precios = {
            '0-100': 'Hasta S/100',
            '101-200': 'S/101 a S/200',
            '201-300': 'S/201 a S/300',
            '301-500': 'S/301 a S/500',
            '500+': 'Más de S/500',
        }
        filtros_activos.append({'tipo': 'precio', 'label': mapa_precios.get(precio, precio)})

    context = {
        'products': products,
        'paginas': paginas,
        'pagina_actual': pagina_actual,

        'marca_actual': marca,
        'uso_actual': uso,
        'condicion_actual': condicion,
        'precio_actual': precio,

        'marcas_opciones': marcas_opciones,
        'uso_opciones': uso_opciones,
        'condicion_opciones': condicion_opciones,
        'precios_opciones': precios_opciones,

        'filtros_activos': filtros_activos,
    }

    return render(request, 'store/lentes_de_contacto.html', context)


def lentes_uso_contacto(request, valor):
    mapa_uso = {
        'diario': 'Diario',
        'mensual': 'Mensual',
        'anual': 'Anual',
        'cosmetico': 'Cosmetico',
    }

    uso_real = mapa_uso.get(valor.lower())
    if not uso_real:
        raise Http404("Uso no encontrao")

    return _render_lentes_de_contacto(request, filtros_iniciales={
        'uso': uso_real
    })   

def lentes_marca_contacto(request, valor):
    mapa_marca = {
        'acuvue': 'Acuvue',
        'air-optix': 'Air-Optix',
        'dailies-aqua': 'Dailies-Aqua',
        'freshlook': 'Freshlook',
        'licryl': 'Licryl',
        'soflens': 'Soflens',
        'purevision': 'Purevision',
        'otros': 'Otros',
    }
    marca_real = mapa_marca.get(valor.lower())
    if not marca_real:
        raise Http404("Marca no encontrada")

    return _render_lentes_de_contacto(request, filtros_iniciales={
        'marca': marca_real
    })

def lentes_condicion_contacto(request, valor):
    mapa_condicion = {
        'miopia-e-hipermetropia': 'Miopia-e-Hipermetropia',
        'astigmatismo': 'Astigmatismo',
        'presbicia': 'Presbicia',
    }

    condicion_real = mapa_condicion.get(valor.lower())
    if not condicion_real:
        raise Http404("Condicion no encontrada")

    return _render_lentes_de_contacto(request, filtros_iniciales={
        'condicion': condicion_real
    })


def buscar_productos(request):
    q = request.GET.get("q", "")
    
    productos = Producto.objects.filter(
        Q(descripcion__icontains=q) |
        Q(cod__icontains=q) |
        Q(marca__icontains=q)
    ).filter(activo=True) if q else []

    return render(request, "store/resultados_busqueda.html", {
        "productos": productos,
        "q": q
    })


def autocomplete_productos(request):
    q = request.GET.get("q", "")
    
    resultados = []

    if q:
        productos = Producto.objects.filter(
            Q(descripcion__icontains=q) |
            Q(cod__icontains=q) |
            Q(marca__icontains=q)
        ).filter(activo=True)[:10]

        for p in productos:
            resultados.append({
                "text": p.descripcion,
                "precio": str(p.precio_venta),
                "url": p.get_absolute_url(),
                "imagen": p.imagenF.url if p.imagenF else ""
            })

    return JsonResponse(resultados, safe=False)


def enviar_mensaje_whatsapp(numero_destino, mensaje):
    token = os.environ.get("WHATSAPP_ACCESS_TOKEN")
    phone_number_id = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")

    url = f"https://graph.facebook.com/v25.0/{phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": numero_destino,
        "type": "text",
        "text": {"body": mensaje},
    }

    return requests.post(url, headers=headers, json=payload)


def menu_principal():
    return """Bienvenido a Óptica IC 👓

Responde con una opción:

1️⃣ Consultar estado de pedido
2️⃣ Horario de atención
3️⃣ Promociones
4️⃣ Hablar con un asesor"""


def obtener_respuesta(mensaje_texto):
    texto = mensaje_texto.strip().lower()

    if texto in ["hola", "buenos dias", "buenos días", "buenas tardes", "buenas noches", "menu", "menú"]:
        return menu_principal()

    if texto == "1":
        return """Para consultar el estado de tu pedido, envíanos tu número de ticket.

Ejemplo:
estado 123"""

    if texto.startswith("estado"):
        partes = texto.split()

        if len(partes) < 2:
            return "Por favor envíanos tu número de recibo. Ejemplo: estado 123"

        numero_pedido = partes[1]

        return f"""Estamos revisando el estado de tu pedido N° {numero_pedido} 👓

En breve un asesor confirmará si ya está listo."""

    if texto == "2":
        return """Nuestro horario de atención es:

Lunes a sábado:
9:00 am. a 7:45 pm.

Domingos y feriados:
10:30 am.a 6:30 pm.

    if texto == "3":
        return """Promociones disponibles en Óptica IC 👓

✅ Promo familiar (3X2 en monturas) 
✅ Consulta por monturas, lunas y multifocales

Escríbenos qué tipo de lentes necesitas."""

    if texto == "4":
        return """Un asesor de Óptica IC te atenderá en breve.

También puedes escribir directamente tu consulta por aquí."""

    return """No entendí tu mensaje.

Responde con una opción del menú:

1️⃣ Consultar estado de pedido
2️⃣ Horario de atención
3️⃣ Promociones
4️⃣ Hablar con un asesor"""


@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "GET":
        mode = request.GET.get("hub.mode", "")
        token = request.GET.get("hub.verify_token", "")
        challenge = request.GET.get("hub.challenge", "")

        if not mode and not token and not challenge:
            return HttpResponse("Webhook WhatsApp activo", status=200)

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(str(challenge), status=200)

        return HttpResponse("Token inválido", status=403)

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            value = data["entry"][0]["changes"][0]["value"]

            if "messages" in value:
                mensaje = value["messages"][0]
                numero_cliente = mensaje.get("from")

                if mensaje.get("type") == "text":
                    texto_cliente = mensaje["text"]["body"]
                    respuesta = obtener_respuesta(texto_cliente)
                else:
                    respuesta = "Por ahora solo puedo responder mensajes de texto. Escribe menú para ver las opciones."

                enviar_mensaje_whatsapp(numero_cliente, respuesta)

        except Exception as e:
            print("ERROR PROCESANDO WHATSAPP:", e)

        return JsonResponse({"status": "ok"})

    return HttpResponse("Método no permitido", status=405)






def suscribir_waba(request):
    token = os.environ.get("WHATSAPP_ACCESS_TOKEN")
    waba_id = "1315153820041937"

    url = f"https://graph.facebook.com/v25.0/{waba_id}/subscribed_apps"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    r = requests.post(url, headers=headers)

    return HttpResponse(
        f"Status: {r.status_code}<br><pre>{r.text}</pre>"
    )