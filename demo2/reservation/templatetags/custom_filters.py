from django import template

register = template.Library()

def split(value, separator=","):
    """
    Divise une chaîne en une liste, selon le séparateur spécifié.
    Par défaut, le séparateur est une virgule (,).
    """
    return value.split(separator)
