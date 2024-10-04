"""
TODO: rellenar

Asignatura: GIW
Práctica 2
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

import csv
import json
from collections import Counter
from pprint import pprint
from geopy.geocoders import Nominatim
from geopy.distance import distance

### Formato CSV
def lee_fichero_accidentes(ruta):
    """
    Lee el fichero de accidentes de tráfico especificado en la ruta
    y devuelve una lista de diccionarios, cada uno representando un accidente.
    
    Cada diccionario contiene las claves 'distrito', 'barrio', 'direccion',
    'tipo', 'fecha', 'hora', 'lesiones_leves', 'lesiones_graves', 'muertes',
    'vehiculos', 'causa' y 'descripcion', con los valores correspondientes
    para cada accidente.
    """
    lista_diccionarios = []
    with open(ruta, 'r', newline='', encoding='utf-8') as fichero:
        diccionario = csv.DictReader(fichero, delimiter=';')
        for linea in diccionario:
            lista_diccionarios.append(linea)

    return lista_diccionarios



def accidentes_por_distrito_tipo(datos):
    """
    Devuelve un contador con el n mero de accidentes que ha habido en cada distrito
    por tipo de accidente, tomando como entrada una lista de diccionarios como el
    primer apartado. Debe devolver un objeto Counter.
    """

    lista =[(dato["distrito"], dato["tipo_accidente"]) for dato in datos]
    counter = Counter(lista)
    pprint(counter)
    return counter


def dias_mas_accidentes(datos):
    """
    Devuelve las fechas del día o días con más accidentes, junto con ese número de accidentes, 
    tomando como entrada una lista de diccionarios como el primer apartado. 
    Debe devolver un conjunto de parejas (días, número de accidentes). """

    lista = {}
    for dia in datos:
        if dia.get('fecha') in lista:
            lista[dia.get('fecha')] += 1
        else:
            lista[dia.get('fecha')] = 1

    max_accidentes = max(lista.values())
    peores_dias = [(fecha, accidentes) for fecha, accidentes in lista.items()
                   if accidentes == max_accidentes]

    return peores_dias

def puntos_negros_distrito(datos, distrito, k):
    """
    Devuelve una lista de tuplas con los k lugares con más accidentes en el distrito
    especificado, siendo cada tupla del estilo (lugar, n mero_de_accidentes), 
    ordenadas de mayor a menor n mero de accidentes y, en caso de empate, alfab ticamente.

    :param datos: lista de diccionarios con la información de los accidentes
    :param distrito: distrito cuyos accidentes se desean analizar
    :param k: n mero de lugares a mostrar
    :return: lista de tuplas con los lugares y n meros de accidentes
    """
    filter_list = []
    for data in datos:
        if data['distrito'] == distrito:
            filter_list.append(data)

    map_it = dict()
    for l in filter_list:
        if l['localizacion'] not in map_it:
            map_it[l['localizacion']] = 1
        else:
            map_it[l['localizacion']] += 1

    list_order = []
    for distrito_map, n_accidentes in map_it.items():
        list_order.append((distrito_map, n_accidentes))

    list_order.sort(key=lambda n: (n[1], n[0]), reverse=True)
    i = 0
    list_final = []
    while i < k:
        list_final.append((list_order[i][0], list_order[i][1]))
        i += 1

    return list_final



#### Formato JSON
def leer_monumentos(ruta):
    """
    Lee el fichero de monumentos en formato JSON especificado en la ruta
    y devuelve una lista de diccionarios, cada uno representando un monumento.

    Cada diccionario contiene las claves 'nombre', 'descripcion', 'address', 'image', 
    'organization-desc', '@id', '@type' y 'type', con los valores 
    correspondientes para cada monumento.
    """
    monumentos = []
    with open(ruta, 'r', encoding='utf-8') as file:
        data = json.load(file)
        monumentos = data.get('@graph')
    return monumentos

def codigos_postales(monumentos):
    """
    Recibe una lista de monumentos y devuelve una lista de tuplas (codigo_postal, num_monumentos)
    ordenada por el n mero de monumentos en cada c digo postal de manera decreciente, y
    por el c digo postal en orden alfabético ascendente en caso de empate.
    """
    cod_postal = [monumento.get('address', {}).get('postal-code','') for monumento in monumentos ]
    num_monumentos = Counter(cod_postal)
    sol = [(codigo_postal, num_monumentos[codigo_postal]) for codigo_postal in num_monumentos]
    sol_ordenada = sorted(sol, key=lambda x: (-x[1], cod_postal.index(x[0])))
    return sol_ordenada


def busqueda_palabras_clave(monumentos, palabras):
    """
    Recibe una lista de monumentos y una lista de palabras clave, y devuelve un conjunto
    de parejas (título, distrito) de aquellos monumentos que contienen las palabras clave en su 
    título o en su descripción (campo 'organization-desc').
    El valor de distrito será la URL almacenada en el campo "@id" dentro de address > district, y si
    este campo no existe el valor de distrito será la cadena vacía. """

    resultado = set()
    for monumento in monumentos:
        for i, palabra in enumerate(palabras):
            buscar_nombre = monumento.get('nombre').lower().find(palabra)
            buscar_descripcion = monumento.get('descripcion').lower().find(palabra)

            if buscar_nombre == -1 and buscar_descripcion == -1:
                break
            if i == len(palabras) - 1:
                resultado.add((monumento.get('nombre'), monumento.get('distrito')))
    return resultado


def busqueda_distancia(monumentos, direccion, distancia):
    """
    Recibe una lista de monumentos, una direcci n y una distancia y devuelve una lista de 
    tuplas (título, id_monumento, distancia) de aquellos monumentos que est n a una distancia 
    menor o igual que la indicada desde la direcci n dada. 

    La lista se ordena por la distancia desde la direcci n dada de manera creciente. 

    La distancia se mide en kil metros.
    """
    geolocator = Nominatim(user_agent="GIW_pr2")
    location = geolocator.geocode(direccion, addressdetails=True)
    coords_original = (location.latitude, location.longitude)
    ternas = []
    i = 0
    while i < len(monumentos):
        m = monumentos[i]
        if 'location' in m and 'latitude' in m['location'] and 'longitude' in m['location']:
            title = m['title']
            id_monumento = m['id']
            latitud = m['location']['latitude']
            longitud = m['location']['longitude']
            coords_monumento = (latitud, longitud)
            calculo_distancia = distance.distance(coords_original, coords_monumento).km
            if calculo_distancia < distancia:
                ternas.append((title, id_monumento, calculo_distancia))
        i += 1
    ternas.sort(key=lambda t: t[2]) #Documnetacion de python ordenar tuplas
    return ternas
