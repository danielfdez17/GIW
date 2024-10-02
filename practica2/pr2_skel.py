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
from geopy import distance

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
    listaDiccionarios = []
    with open(ruta, 'r', newline='', encoding='utf-8') as fichero:
        diccionario = csv.DictReader(fichero, delimiter=';')
        for linea in diccionario:
            listaDiccionarios.append(linea)

    return listaDiccionarios



def accidentes_por_distrito_tipo(datos):
    lista =[(dato["distrito"], dato["tipo_accidente"]) for dato in datos]
    counter = Counter(lista)
    pprint(counter)
    return counter
    

def dias_mas_accidentes(datos):
    ...

def puntos_negros_distrito(datos, distrito, k):
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
    monumentos = []
    with open(ruta, 'r', encoding='utf-8') as file:
        data = json.load(file)
        monumentos = data.get('@graph')
    return monumentos

def codigos_postales(monumentos):
    ...

def busqueda_palabras_clave(monumentos, palabras):
    ...

def busqueda_distancia(monumentos, direccion, distancia):
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


