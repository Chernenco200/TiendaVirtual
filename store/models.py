from django.utils.text import slugify
from django.urls import reverse


from django.contrib.auth.models import User
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django_resized import ResizedImageField

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name



class Formas(models.Model):
	forma = models.CharField(max_length=200)
	
	def __str__(self):
		return self.forma

class Generos(models.Model):
	genero=models.CharField(max_length=200)
	def __str__(self):
		return self.genero

class Colores(models.Model):
	color = models.CharField(max_length=200)
	def __str__(self):
		return self.color

class Marcas(models.Model):
	marca = models.CharField(max_length=200)
	def __str__(self):
		return self.marca

class Materiales(models.Model):
	material = models.CharField(max_length=200)
	def __str__(self):
		return self.material

		
class Tallas(models.Model):
	talla = models.CharField(max_length=200)
	def __str__(self):
		return self.talla

class Clases(models.Model):
	clase = models.CharField(max_length=200)
	def __str__(self):
		return self.clase

class Usos(models.Model):
	uso = models.CharField(max_length=200)
	def __str__(self):
		return self.uso

class Tipos(models.Model):
	tipo = models.CharField(max_length=200)
	def __str__(self):
		return self.tipo

class Marcacontactos(models.Model):
	marcacontacto = models.CharField(max_length=200)
	def __str__(self):
		return self.marcacontacto

class Product(models.Model):
	nuevo = models.BooleanField(default=False,null=True, blank=True)
	name = models.CharField(max_length=200)
	cod=models.CharField(max_length=10)
	price = models.FloatField()
	digital = models.BooleanField(default=False,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	image2 = models.ImageField(null=True, blank=True)
	image3 = models.ImageField(null=True, blank=True)
	forma = models.ForeignKey(Formas, on_delete=models.SET_NULL, null=True, blank=True)
	genero = models.ForeignKey(Generos, on_delete=models.SET_NULL, null=True, blank=True)
	color = models.ForeignKey(Colores, on_delete=models.SET_NULL, null=True, blank=True)
	marca = models.ForeignKey(Marcas, on_delete=models.SET_NULL, null=True, blank=True)
	material = models.ForeignKey(Materiales, on_delete=models.SET_NULL, null=True, blank=True)
	talla = models.ForeignKey(Tallas, on_delete=models.SET_NULL, null=True, blank=True)
	clase = models.ForeignKey(Clases, on_delete=models.SET_NULL, null=True, blank=True)
	disponible = models.BooleanField(default=True,null=True, blank=True)
	uso = models.ForeignKey(Usos, on_delete=models.SET_NULL, null=True, blank=True)
	tipo = models.ForeignKey(Tipos, on_delete=models.SET_NULL, null=True, blank=True)
	marcacontacto = models.ForeignKey(Marcacontactos, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
	
	def image2URL(self):
		try:
			url = self.image2.url
		except:
			url = ''
		return url

	def image3URL(self):
		try:
			url = self.image3.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address














TODAY = date.today()
# Create your models here.

ESTADOS = ( 
	("Programado", "Programado"), 
	("En espera", "En espera"), 
	("En proceso", "En proceso"), 
	("Atrasado", "Atrasado"),  
	("Realizado", "Realizado")
	)

UNIDAD_COMPRA = ( 
	("Pieza", "Pieza"),  
	("Kg", "Kg"), 
	("gramos", "gramos"),
	("Lt", "Lt"), 
	("Metro", "Metro"),  
	("Caja", "Caja"), 
	("Onza", "Onza"),
	("Charola", "Charola"),
	("Otro", "Otro")
	)






class Producto(models.Model):
    TIPO_CHOICES = [
        ('Monturas oftálimcas', 'Monturas oftálimcas'),
        ('Monturas Solares', 'Monturas Solares'),
        ('Lentes de Contacto', 'Lentes de Contacto'),
        ('Monturas de Marca', 'Monturas de Marca'),
        ('Líquidos', 'Líquidos'),
        ('Accesorios', 'Accesorios'),  
    ]

    CATEGORIA_CHOICES = [
        ('Mujer', 'Mujer'),
        ('Hombre', 'Hombre'),
        ('Nino', 'Nino'), 
    ]

    FORMA_CHOICES = [
        ('Agatado', 'Agatado'),
        ('Almendra', 'Almendra'),
        ('Aviador', 'Aviador'),
        ('Cuadrado', 'Cuadrado'),
        ('Redondo', 'Redondo'),
        ('Exagonal', 'Exagonal'),
        ('Otros', 'Otros'),  
    ]

    MATERIAL_CHOICES = [
        ('Fibra de carbono', 'Fibra de carbono'),
        ('Acetato', 'Acetato'),
        ('Carey', 'Carey'),
        ('TR90', 'TR90'),
        ('Aluminium', 'Aluminium'),
        ('Engomado', 'Engomado'),
        ('Otros', 'Otros'),  
    ]
    MARCA_CHOICES = [
        ('Ray-Ban', 'Ray-Ban'),
        ('OaKley', 'OaKley'),
        ('Nike', 'Nike'),
        ('Guess', 'Guess'),
        ('Tommy-Hilfiger', 'Tommy-Hilfiger'),
        ('Arnette', 'Arnette'),
        ('Nano', 'Nano'),
        ('Otros', 'Otros'),

        ('Acuvue', 'Acuvue'),
        ('Air-Optix', 'Air-Optix'),
        ('Dailies-Aqua', 'Dailies-Aqua'),
        ('Freshlook', 'Freshlook'),
        ('Licryl', 'Licryl'),
        ('Soflens', 'Soflens'),
        ('Purevision', 'Purevision'),
		('Otros', 'Otros'),
		
    ]
    CONDICION_CHOICES = [
        ('Miopia-e-Hipermetropia', 'Miopia-e-Hipermetropia'),
        ('Astigmatismo', 'Astigmatismo'),
        ('Presbicia', 'Presbicia'),
    ]

    USO_CHOICES = [
        ('Diario', 'Diario'),
        ('Mensual', 'Mensual'),
        ('Anual', 'Anual'),
        ('Cosmetico', 'Cosmetico'),
    ]

    TALLA_CHOICES = [
        ('Grande', 'Grande'),
        ('Mediana', 'Mediana'),
        ('Chica', 'Chica'),
    ]

    cod = models.CharField(max_length=20, unique=True)  # por ej. COD-001
    tipo= models.CharField(max_length=50, choices=TIPO_CHOICES, null=True, blank=True)
    nuevo = models.BooleanField(default=False, null=True, blank=True)
    marca = models.CharField(max_length=20, choices=MARCA_CHOICES, blank=True, null=True)
    categoria= models.CharField(max_length=20, choices=CATEGORIA_CHOICES, null=True, blank=True)
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES, null=True, blank=True)
    forma = models.CharField(max_length=20, choices=FORMA_CHOICES, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)   
    talla_luna = models.CharField(max_length=5, null=True, blank=True)    
    puente = models.CharField(max_length=5, null=True, blank=True)
    largo = models.CharField(max_length=5, null=True, blank=True)
    ancho = models.CharField(max_length=5, null=True, blank=True)
    altura = models.CharField(max_length=5, null=True, blank=True)    
    descripcion = models.CharField(max_length=200, null=True, blank=True)              # ej. LUNA BLANCA 1.56
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(default=0, blank=True, null=True)                 # stock actual
    talla = models.CharField(max_length=50, choices=TALLA_CHOICES, null=True, blank=True)       # si aplica
    activo = models.BooleanField(default=True, blank=True, null=True)             # por si luego das de baja productos   
    costo_promedio = models.DecimalField(max_digits=10, decimal_places=4, default=0, blank=True, null=True)
    imagenF = models.ImageField(upload_to="productos/", blank=True, null=True)
    imagenD = models.ImageField(upload_to="productos/", blank=True, null=True)
    imagenL = models.ImageField(upload_to="productos/", blank=True, null=True)
    condicion = models.CharField(max_length=50, choices=CONDICION_CHOICES, null=True, blank=True)
    uso = models.CharField(max_length=20, choices=USO_CHOICES, null=True, blank=True)

    slug = models.SlugField(max_length=300, unique=True, blank=True, null=True)
  
    class Meta:
        db_table = "core_producto"   # 🔴 IMPORTANTE: nombre real de la tabla
    #    managed = False              # 🔴 NO crear ni modificar esta tabla


    def __str__(self):
        return f"{self.cod} - {self.descripcion}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base = f"{self.marca or ''} {self.descripcion or ''} {self.cod or ''}".strip()
            self.slug = slugify(base)

        original_slug = self.slug
        contador = 1
        while Producto.objects.exclude(pk=self.pk).filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{contador}"
            contador += 1

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('producto_detalle', kwargs={'slug': self.slug})    



class Valoracion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='valoraciones')
    puntuacion = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto.descripcion} - {self.puntuacion}"
