from django import template

register = template.Library()

@register.simple_tag
def my_url(value, field_nombre, urlencode=None):
    url = '?{}={}'.format(field_nombre, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_nombre, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


# Textos legibles para títulos SEO: "Tommy-Hilfiger" -> "Tommy Hilfiger",
# "Miopia-e-Hipermetropia" -> "miopía e hipermetropía"
_TEXTOS_SEO = {
    "Ray-Ban": "Ray-Ban",
    "Nino": "niños",
    "Miopia-e-Hipermetropia": "miopía e hipermetropía",
    "Cosmetico": "cosmético",
}


@register.filter
def texto_seo(value):
    if not value:
        return ""
    value = str(value)
    return _TEXTOS_SEO.get(value, value.replace("-", " "))
