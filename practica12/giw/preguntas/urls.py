"""
Definición de las rutas de la app, enlazando las funciones que las manejan
"""
from django.urls import path
from preguntas import views

app_name = "preguntas"

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginfunction, name='login'),
    path('logout', views.logoutfunction, name='logout'),
    path('', views.index, name='ver_preguntas'),
    path('<int:id>', views.nueva_respuesta, name='detalle_pregunta'),
    path('nueva_pregunta', views.nueva_pregunta, name='nueva_pregunta'),
]
