"""
Fichero con los filtros personalizados"""
from django import template
from django.utils.timezone import localtime

register = template.Library()

"""
Agregamos un filtro customizado para
poder modificar los caracteres de la fecha
"""
@register.filter
def formato_fecha(fecha):
    """
    Devuelve la fecha en el formato deseado"""
    fecha_local = localtime(fecha)
    fecha_formateada = fecha_local.strftime("%d de %B de %Y a las %H:%M")
    month_capitalize = fecha_local.strftime("%B").capitalize()
    return fecha_formateada.replace(fecha_local.strftime("%B"), month_capitalize)
