# TODO: rellenar
# Asignatura: GIW
# Práctica 3
# Grupo: 05
# Autores: 
# - Luis Enrique Barrero Peña
# - Daniel Fernández Ortiz
# - Airam Martín Peraza
# - José Waldo Villacres Zumaeta 
#
# Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
# sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
# de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
# de manera directa o indirecta. Declaramos además que no hemos realizado de manera
# deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
# resultados de los demás.

import xml.sax
import html
from pprint import pprint


def nombres_restaurantes(filename):
    class ManejadorNombresRestaurantes(xml.sax.ContentHandler):
        
        def __init__(self):
            self.texto = ""
            self.lista = []

        # def startDocument(self):

        # def endDocument(self):
            
        def startElement(self, etiqueta, atributos):
            self.texto = ""
        def characters(self, contenido):
            self.texto += contenido
                
        def endElement(self, etiqueta):
            if etiqueta == "name":
                self.lista.append(html.unescape(self.texto.strip()))

        def getLista(self):
            return self.lista

    parser = xml.sax.make_parser()
    manejador = ManejadorNombresRestaurantes()
    parser.setContentHandler(manejador)
    parser.parse(filename)
    return sorted(manejador.getLista())

# pprint(nombres_restaurantes("practica3/restaurantes_v1_es_pretty.xml"))
# pprint(nombres_restaurantes("practica3/restaurantes_v1_es.xml"))




def subcategorias(filename):
    ...


def info_restaurante(filename, name):
    ...


def busqueda_cercania(filename, lugar, n):
    ...
