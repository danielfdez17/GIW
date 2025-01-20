"""
Definición de formularios para validación
"""
from django import forms
# from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    """Formulario para autenticar usuarios"""
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Contraseña', max_length=100, widget=forms.PasswordInput)

class PreguntaForm(forms.Form):
    """Formulario para crear una nueva pregunta"""
    titulo = forms.CharField(label='Titulo')
    text = forms.CharField(label='Pregunta')

class RespuestaForm(forms.Form):
    """Formulario para crear una nueva respuesta a una pregunta"""
    texto = forms.CharField(label='Respuesta', max_length=5000, widget=forms.Textarea)
