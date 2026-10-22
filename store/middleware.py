from urllib.parse import urlsplit

from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class DominioCanonicoMiddleware:
    """
    Redirige (301) cualquier visita que llegue por otro dominio
    (app-tienda-virtual-....herokuapp.com, o la variante con/sin www)
    al dominio oficial definido en SITE_URL. Así Google ve un solo sitio.
    """

    HOSTS_LOCALES = {"localhost", "127.0.0.1"}

    def __init__(self, get_response):
        self.get_response = get_response
        self.host_oficial = urlsplit(settings.SITE_URL).netloc.lower()

    def __call__(self, request):
        host = request.get_host().split(":")[0].lower()
        if (
            not settings.DEBUG
            and self.host_oficial
            and host != self.host_oficial
            and host not in self.HOSTS_LOCALES
            and request.method in ("GET", "HEAD")
        ):
            return HttpResponsePermanentRedirect(f"{settings.SITE_URL}{request.get_full_path()}")
        return self.get_response(request)
