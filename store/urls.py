from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.home, name="home"),
	path('home/', views.home, name="home"),
	path('lentes-oftalmicos/', views.lentes_oftalmicos, name="lentes_oftalmicos"),

    path('lentes-de-sol/', views.lentes_de_sol, name="lentes_de_sol"),

    path('lentes-de-contacto/', views.lentes_de_contacto, name="lentes_de_contacto"),

	path('legal/', views.legal, name="legal"),
    path('nosotros/', views.nosotros, name="nosotros"),


    #CEO
    path('lentes-oftalmicos/<slug:slug>/', views.producto_detalle, name='producto_detalle'),
    path('lentes-de-sol/<slug:slug>/', views.producto_detalle, name='producto_detalle'),
    path('lentes-de-contacto/<slug:slug>/', views.producto_detalle, name='producto_detalle'),
    path('detalle/<slug:slug>/', views.producto_detalle, name='producto_detalle'),

   #---------oftalmicos---------
    path(
        'lentes-oftalmicos/genero/<slug:valor>/',
        views.lentes_categoria,
        name='lentes_categoria'
    ),

    path(
        'lentes-oftalmicos/forma/<slug:valor>/',
        views.lentes_forma,
        name='lentes_forma'
    ),

    path(
        'lentes-oftalmicos/marca/<slug:valor>/',
        views.lentes_marca,
        name='lentes_marca'
    ),

        path(
        'lentes-oftalmicos/talla/<slug:valor>/',
        views.lentes_talla,
        name='lentes_talla'
    ),

   #---------Solares---------
    path(
        'lentes-de-sol/genero/<slug:valor>/',
        views.gafas_genero,
        name='gafas_genero'
    ),

    path(
        'lentes-de-sol/forma/<slug:valor>/',
        views.gafas_forma,
        name='gafass_forma'
    ),

    path(
        'lentes-de-sol/marca/<slug:valor>/',
        views.gafas_marca,
        name='gafas_marca'
    ),

    path(
        'lentes-de-sol/talla/<slug:valor>/',
        views.gafas_talla,
        name='gafas_talla'
    ),

   #---------Contacto---------
    path(
        'lentes-de-contacto/marca/<slug:valor>/',
        views.lentes_marca_contacto,
        name='lentes_marca_contacto'
    ),

    path(
        'lentes-de-contacto/uso/<slug:valor>/',
        views.lentes_uso_contacto,
        name='lentes_uso_contacto'
    ),

    path(
        'lentes-de-contacto/condicion/<slug:valor>/',
        views.lentes_condicion_contacto,
        name='lentes_condicion_contacto'
    ),


]