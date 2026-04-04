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
    