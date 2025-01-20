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
import xml.dom
import xml.dom.minicompat
import xml.dom.minidom
import xml.sax
import html
from xml.etree import ElementTree
from geopy.geocoders import Nominatim
#from geopy.distance import distance
# Da error en tiempo de ejecucion porque no encuentra la clase distance, con geodesic si deja
from geopy.distance import geodesic
# from pprint import pprint


def nombres_restaurantes(filename):
    """
    Lee un archivo XML que describe una lista de restaurantes y devuelve una
    lista ordenada alfabéticamente con los nombres de los restaurantes.

    :param filename: Ruta del archivo XML que contiene la lista de restaurantes
    :return: Una lista ordenada alfabéticamente con los nombres de los restaurantes
    """
    class ManejadorNombresRestaurantes(xml.sax.ContentHandler):
        """
        Manejador que procesa las etiquetas 'name' del archivo xml pasado por parámetro
        y las almacena en una lista
        """
        def __init__(self):
            super().__init__()
            self.texto = ""
            self.lista = []

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


def subcategorias(filename):
    """
    Lee un archivo XML que describe un catálogo y devuelve un conjunto con todas
    las subcategorías del catálogo, representadas como cadenas en formato
    "categoria > subcategoria".

    :param filename: Ruta del archivo XML que contiene el catálogo
    :return: Un conjunto con todas las subcategorías del catálogo
    """
    class ManejadorCatalogo (xml.sax.ContentHandler):
        """
        Manejador que procesa las etiquetas 'item' del archivo xml pasado por parámetro
        almacenándolas en un conjunto
        """
        def __init__(self):
            super().__init__()
            self.curr_path = []
            self.texto = ""
            self.conjunto = set()
            self.categoria = ""
            self.subcategoria = ""
            self.dentro_categoria = False
            self.dentro_subcategoria = False

        def startElement(self, name, attrs):
            self.curr_path.append(name)
            self.texto = ""
            if name == "item" and attrs.get("name") == "Categoria":
                self.dentro_categoria = True
            elif name == "item" and attrs.get("name") == "SubCategoria":
                self.dentro_subcategoria = True

        def characters(self, content):
            self.texto += content

        def endElement(self, name):
            if name == "item" and self.dentro_categoria:
                self.categoria = self.texto
                self.dentro_categoria = False
            elif name == "item" and self.dentro_subcategoria:
                self.subcategoria = self.texto
                self.conjunto.add(f"{self.categoria} > {self.subcategoria}")
                self.dentro_subcategoria = False

    parser = xml.sax.make_parser()
    manejador = ManejadorCatalogo()
    parser.setContentHandler(manejador)
    parser.parse(filename)
    return manejador.conjunto

def info_restaurante(filename, name):
    """
    Utilizando DOM o ElementTree,, recibe la ruta del fichero XML y un nombre de un restaurante 
    y devuelve un diccionario Python con la información básica del restaurante.

    Si alguno de los campos no existe se devolverá None, y si no hay ningún restaurante con 
    ese nombre se devolverá None en vez de un diccionario.
    Lee un archivo XML que describe una lista de restaurantes y devuelve una
    lista ordenada alfabéticamente con los nombres de los restaurantes.

    """

    dicc_rest = {}
    tree = ElementTree.parse(filename)
    root =  tree.getroot()

    for restaurante in root.findall('.//service'):
        info = restaurante.find('basicData')
        nombre_restaurante = info.find('name')

        if nombre_restaurante is not None and nombre_restaurante.text == name:
            dicc_rest['nombre'] = name

            descripcion = info.find('body')
            if descripcion is not None and descripcion.text is not None:
                dicc_rest['descripcion'] = html.unescape(descripcion.text)
            else:
                dicc_rest['descripcion'] = None

            email = info.find('email')
            if email is not None and email.text is not None:
                dicc_rest['email'] = html.unescape(email.text)
            else:
                dicc_rest['email'] = None

            web = info.find('web')
            if web is not None and web.text is not None:
                dicc_rest['web'] = html.unescape(web.text)
            else:
                dicc_rest['web'] = None

            phone = info.find('phone')
            if phone is not None and phone.text is not None:
                dicc_rest['phone'] = html.unescape(phone.text)
            else:
                dicc_rest['phone'] = None

            extra_info = restaurante.find('extradata')
            horario = None
            if extra_info is not None:
                for item in extra_info.findall('item'):
                    if item.get('name') == 'Horario' and item.text is not None:
                        horario = html.unescape(item.text)

            dicc_rest['horario'] = horario

            return dicc_rest

    return None

def is_float(n):
    """
        Función auxiliar que comprueba que si es numero float o no
        Devuelve False en caso de no ser Float
    """
    try:
        float(n)
        return True
    except FloatingPointError:
        return False

def busqueda_cercania(filename, lugar, n):
    """
        Metodo que devuelve una lista de parejas(distancia, nombre_restaurante) 
        ordenadas de lugar de distancia mas cercana a mas lejano
        con un numero de 'n' de km, y por ultimo debe desescapara el texto HTML escapado 
        en los nombres de los restaurantes es decir convertir
        entidades HTML en caracter normal.
        En caso de no existir el lugar introducido o no se encuentre el archivo 
        se devolvera una lista vacia.
        En caso de que no exista el elemento basicData o geoData, 
        y en caso de que el elemento nombre
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
    except xml.etree.ElementTree.ParseError:
        return []

    restaurantes_tuple = []
    for  _, service in enumerate(raiz.findall("./service")):

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
