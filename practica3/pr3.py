"""
 TODO: rellenar
 Asignatura: GIW
 Práctica 3
 Grupo: 05
 Autores:
 - Luis Enrique Barrero Peña
 - Daniel Fernández Ortiz
 - Airam Martín Peraza
 - José Waldo Villacres Zumaeta

 Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
 sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
 de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
 de manera directa o indirecta. Declaramos además que no hemos realizado de manera
 deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
 resultados de los demás.
"""
import xml.sax
import html
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from xml.etree import ElementTree
# from pprint import pprint


def nombres_restaurantes(filename):
    """
    Lee un archivo XML que describe una lista de restaurantes y devuelve una
    lista ordenada alfabéticamente con los nombres de los restaurantes.

    :param filename: Ruta del archivo XML que contiene la lista de restaurantes
    :return: Una lista ordenada alfabéticamente con los nombres de los restaurantes
    """
    class ManejadorNombresRestaurantes(xml.sax.ContentHandler):
        """adf"""
        def __init__(self):
            self.texto = ""
            self.lista = []

        # def startDocument(self):

        # def endDocument(self):

        def startElement(self, name, attrs):
            self.texto = ""
        def characters(self, content):
            self.texto += content

        def endElement(self, name):
            if name == "name":
                self.lista.append(html.unescape(self.texto.strip()))

        def get_lista(self):
            """
            Devuelve la lista de nombres de restaurantes
            """
            return self.lista

    parser = xml.sax.make_parser()
    manejador = ManejadorNombresRestaurantes()
    parser.setContentHandler(manejador)
    parser.parse(filename)
    return sorted(manejador.get_lista())

# def subcategorias(filename):
    # ...


# def info_restaurante(filename, name):
    # ...


def busqueda_cercania(filename, lugar, n):
    """
        Metodo que devuelve una lista de parejas(distancia, nombre_restaurante) ordenadas de lugar de distancia mas cercana a mas lejano
        con un numero de 'n' de km, y por ultimo debe desescapara el texto HTML escapado en los nombres de los restaurantes es decir convertir
        entidades HTML en caracter normal.
    """
    geolocator = Nominatim(user_agent="GIW_pr3")
    location = geolocator.geocode(lugar, addressdetails=True)    
    
    if not location:
        return []

    coords_lugar = (location.latitude, location.longitude)
    arbol = ElementTree.parse(filename)
    raiz = arbol.getroot()
    restaurantes_tuple = []
    for  i, service in enumerate(raiz.findall("./service")):
        nombre_restaurante = service.find("./basicData/name").text #Nos introducimos en un objeto de basicData y luego een el campo 'name'
        latitud = service.find("./geoData/latitude").text
        longitud = service.find("./geoData/longitude").text
        if latitud is not None and longitud is not None: #Checkeamos que no sean vacios
            coords_restaurante = (float(latitud), float(longitud))
            calculo_distancia = geodesic(coords_lugar, coords_restaurante).km
            if calculo_distancia <= n:
                nombre_restaurante = html.unescape(nombre_restaurante)
                restaurantes_tuple.append((calculo_distancia, nombre_restaurante))
    
    restaurantes_tuple.sort()
    return restaurantes_tuple