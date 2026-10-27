from django.contrib.sitemaps import Sitemap

from .models import Producto

TIPO_OFTALMICO = "Monturas oftálmicas"
TIPO_SOL = "Monturas Solares"
TIPO_CONTACTO = "Lentes de Contacto"

# (prefijo de URL, tipo de producto, campo del modelo, {slug: valor})
# Deben coincidir con los "mapa_..." de views.py
GENEROS = {"hombre": "Hombre", "mujer": "Mujer", "nino": "Nino"}
FORMAS = {"agatado": "Agatado", "almendra": "Almendra", "piloto": "Piloto", "cuadrado": "Cuadrado",
          "redondo": "Redondo", "exagonal": "Exagonal"}
MARCAS = {"ray-ban": "Ray-Ban", "nike": "Nike", "oakley": "Oakley", "guess": "Guess",
          "tommy-hilfiger": "Tommy-Hilfiger", "arnette": "Arnette", "nano": "Nano", "razza": "Razza",
          "lacoste": "Lacoste", "skechers": "Skechers"}
TALLAS = {"grande": "Grande", "mediana": "Mediana", "chica": "Chica"}

PAGINAS_FILTRO = [
    ("/lentes-oftalmicos/genero/", TIPO_OFTALMICO, "categoria", GENEROS),
    ("/lentes-oftalmicos/forma/", TIPO_OFTALMICO, "forma", FORMAS),
    ("/lentes-oftalmicos/marca/", TIPO_OFTALMICO, "marca", MARCAS),
    ("/lentes-oftalmicos/talla/", TIPO_OFTALMICO, "talla", TALLAS),
    ("/lentes-de-sol/genero/", TIPO_SOL, "categoria", GENEROS),
    ("/lentes-de-sol/forma/", TIPO_SOL, "forma", FORMAS),
    ("/lentes-de-sol/marca/", TIPO_SOL, "marca", MARCAS),
    ("/lentes-de-sol/talla/", TIPO_SOL, "talla", TALLAS),
    ("/lentes-de-contacto/uso/", TIPO_CONTACTO, "uso",
     {"diario": "Diario", "mensual": "Mensual", "anual": "Anual", "cosmetico": "Cosmetico"}),
    ("/lentes-de-contacto/marca/", TIPO_CONTACTO, "marca",
     {"acuvue": "Acuvue", "air-optix": "Air-Optix", "dailies-aqua": "Dailies-Aqua", "freshlook": "Freshlook",
      "licryl": "Licryl", "soflens": "Soflens", "purevision": "Purevision"}),
    ("/lentes-de-contacto/condicion/", TIPO_CONTACTO, "condicion",
     {"miopia-e-hipermetropia": "Miopia-e-Hipermetropia", "astigmatismo": "Astigmatismo",
      "presbicia": "Presbicia"}),
]


def _disponibles():
    # Solo productos activos, con stock y con foto principal.
    # Cuando subes la foto en facturación, el producto entra solo al sitemap.
    return (Producto.objects.filter(activo=True, stock__gte=1)
            .exclude(imagenF__isnull=True).exclude(imagenF=""))


class PaginasPrincipalesSitemap(Sitemap):
    protocol = "https"
    changefreq = "weekly"

    def items(self):
        return [
            ("/", 1.0),
            ("/lentes-oftalmicos/", 0.9),
            ("/lentes-de-sol/", 0.9),
            ("/lentes-de-contacto/", 0.9),
            ("/nosotros/", 0.4),
            ("/legal/", 0.2),
        ]

    def location(self, item):
        return item[0]

    def priority(self, item):
        return item[1]


class PaginasFiltroSitemap(Sitemap):
    """Páginas como /lentes-oftalmicos/marca/ray-ban/ (solo si tienen productos)."""
    protocol = "https"
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        urls = []
        base = _disponibles()
        for prefijo, tipo, campo, valores in PAGINAS_FILTRO:
            for slug, valor in valores.items():
                if base.filter(tipo=tipo, **{f"{campo}__iexact": valor}).exists():
                    urls.append(f"{prefijo}{slug}/")
        return urls

    def location(self, item):
        return item


class ProductosSitemap(Sitemap):
    protocol = "https"
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        # Igual que los catálogos: solo productos con foto principal
        return (_disponibles()
                .exclude(slug__isnull=True).exclude(slug="")
                .exclude(imagenF__isnull=True).exclude(imagenF="")
                .order_by("pk"))


SITEMAPS = {
    "principales": PaginasPrincipalesSitemap,
    "filtros": PaginasFiltroSitemap,
    "productos": ProductosSitemap,
}
