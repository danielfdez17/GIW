"""
Fichero con la definición de los modelos para el ORM
"""
from django.db import models
from django.conf import settings
from django.utils.html import escape

# Create your models here.
class Pregunta(models.Model):
    """Modelo para almacenar las preguntas de los usuarios"""
    id = models.BigAutoField(primary_key=True, null=False)
    titulo = models.CharField(max_length=250, null=False)
    texto = models.TextField(max_length=5000, null=False)
    fecha = models.DateTimeField(auto_now_add=True, null=False)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def num_respuestas(self):
        """Devuelve el número de respuestas de la pregunta"""
        return self.respuesta_set.count()

    def clean(self):
        self.titulo = escape(self.titulo)
        self.texto = escape(self.texto)

class Respuesta(models.Model):
    """Modelo para almacenar las respuestas de los usuarios"""
    id = models.BigAutoField(primary_key=True, null=False)
    texto = models.TextField(max_length=5000, null=False)
    fecha = models.DateTimeField(auto_now_add=True, null=False)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)

    def clean(self):
        self.texto = escape(self.texto)
