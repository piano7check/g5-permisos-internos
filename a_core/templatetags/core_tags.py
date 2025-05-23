from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter para obtener un valor de un diccionario por su clave
    """
    return dictionary.get(key) 