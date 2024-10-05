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
#from geopy.distance import distance Da error en tiempo de ejecucion porque no encuentra la clase distance, con geodesic si deja
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


"""
    Funcion auxiliar que comprueba que si es numero float o no
    Devuelve False en caso de no ser Float
"""
def is_float(n):
    try:
        float(n)
        return True
    except Exception:
        return False

def busqueda_cercania(filename, lugar, n):
    """
        Metodo que devuelve una lista de parejas(distancia, nombre_restaurante) ordenadas de lugar de distancia mas cercana a mas lejano
        con un numero de 'n' de km, y por ultimo debe desescapara el texto HTML escapado en los nombres de los restaurantes es decir convertir
        entidades HTML en caracter normal.
        En caso de no existir el lugar introducido o no se encuentre el archivo 
        se devolvera una lista vacia.
        En caso de que no exista el elemento basicData o geoData, y en caso de que el elemento nombre
        de basicData, o la longitud o la latitud no sean numeros decimales, ignoraremos la iteracion 
    """
    geolocator = Nominatim(user_agent="GIW_pr3")
    location = geolocator.geocode(lugar, addressdetails=True)    
    
    if not location:
        return []

    coords_lugar = (location.latitude, location.longitude)
    
    try:
        arbol = ElementTree.parse(filename)
        raiz = arbol.getroot()
    except Exception:
        return []

    restaurantes_tuple = []
    for  i, service in enumerate(raiz.findall("./service")):
        
        basic_data = service.find("basicData")
        geo_data = service.find("geoData")
        if basic_data is None or geo_data is None:
            continue
        
        nombre_restaurante = basic_data.find("name").text
        if nombre_restaurante is None:
            continue
        
        latitud = geo_data.find("latitude").text
        longitud = geo_data.find("longitude").text
        if not is_float(latitud) or not is_float(longitud):
            continue

        coords_restaurante = (float(latitud), float(longitud))
        calculo_distancia = geodesic(coords_lugar, coords_restaurante).km
        if calculo_distancia <= n:
            nombre_restaurante = html.unescape(nombre_restaurante)
            restaurantes_tuple.append((calculo_distancia, nombre_restaurante))
    
    restaurantes_tuple.sort()
    return restaurantes_tuple