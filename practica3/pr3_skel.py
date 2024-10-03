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

        self.num_evento += 1

def nombres_restaurantes(filename):
    class ManejadorNombresRestaurantes(xml.sax.ContentHandler):
        
        def __init__(self):
            self.tabulador = ""
            self.num_evento = 1

        def startDocument(self):
            print(f'{self.tabulador}{self.num_evento}) **Inicio de documento**')
            self.num_evento += 1

        def endDocument(self):
            print(f'{self.tabulador}{self.num_evento}) **Fin de documento**')
            self.num_evento += 1
            
        def startElement(self, etiqueta, atributos):
            print(f'{self.tabulador}{self.num_evento}) Inicio de etiqueta <{etiqueta}> con atributos {atributos.items()}')
            self.tabulador += "    "  # Aumenta la sangría
            self.num_evento += 1

        def characters(self, contenido):
            print(f'{self.tabulador}{self.num_evento}) Leyendo cadena de caracteres: "{contenido}"')
            self.num_evento += 1
                
        def endElement(self, etiqueta):
            self.tabulador = self.tabulador[:-4]  # Reduce la sangría
            print(f'{self.tabulador}{self.num_evento}) Final de etiqueta <{etiqueta}>')


def subcategorias(filename):
    ...


def info_restaurante(filename, name):
    ...


def busqueda_cercania(filename, lugar, n):
    ...
