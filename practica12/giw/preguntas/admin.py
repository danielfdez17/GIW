"""
Fichero para registrar qué objetos se manejaran en la interfaz de administración
"""
from django.contrib import admin
from preguntas.models import Pregunta, Respuesta

# Register your models here.
admin.site.register(Pregunta)
admin.site.register(Respuesta)
