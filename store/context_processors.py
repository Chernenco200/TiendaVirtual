from django.conf import settings


def seo(request):
    """Datos para las etiquetas SEO de main.html."""
    site_url = settings.SITE_URL
    pagina = request.GET.get("page")
    canonical = f"{site_url}{request.path}"
    if pagina and pagina != "1":
        canonical += f"?page={pagina}"
    return {
        "SITE_URL": site_url,
        "SITE_NAME": "Ópticas IC",
        "canonical_url": canonical,
    }
