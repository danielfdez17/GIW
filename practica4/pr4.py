"""
TODO: rellenar

Asignatura: GIW
Práctica 4
Grupo: 5
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
import sys
import os
import sqlite3
from datetime import datetime
import csv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def crear_bd(db_filename):
    """
    Crea una base de datos con dos tablas, datos_generales y semanales_IBEX35, en
    el archivo db_filename. La tabla datos_generales tiene como columnas ticker,
    nombre, índice y país; la tabla semanales_IBEX35 tiene como columnas ticker,
    fecha, precio, y una clave foránea a la columna ticker de datos_generales
    y una clave primaria compuesta por ticker y fecha.

    Devuelve la conexión abierta con la base de datos.

    :param db_filename: Fichero que se utilizará como BD
    :return: La conexión abierta con las tablas ya creadas
    """
    conn = sqlite3.connect(db_filename)

    conn.execute("DROP TABLE IF EXISTS datos_generales")
    conn.execute("""
        CREATE TABLE datos_generales (
            ticker TEXT PRIMARY KEY,
            nombre TEXT,
            indice TEXT,
            pais TEXT)
    """)

    conn.execute("DROP TABLE IF EXISTS semanales_IBEX35")
    conn.execute("""
        CREATE TABLE semanales_IBEX35 (
            ticker TEXT,
            fecha TEXT,
            precio REAL,
            FOREIGN KEY(ticker) REFERENCES datos_generales(ticker),
            PRIMARY KEY (ticker, fecha))
    """)

    conn.commit()
    return conn

def transformar_fecha(fecha):
    """
    Transforma una fecha desde el formato "%d/%m/%Y %H:%M" al formato "%Y-%m-%d %H:%M".

    Devuelve la fecha transformada como cadena.

    :param fecha: Fecha a transformar como cadena.
    :return: Fecha transformada como cadena.
    """
    formato_entrada = "%d/%m/%Y %H:%M"
    formato_salida = "%Y-%m-%d %H:%M"
    fecha_obj = datetime.strptime(fecha, formato_entrada)
    return fecha_obj.strftime(formato_salida)

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

def cargar_bd(db_filename, tab_datos, tab_ibex35):
    """
    Carga las tablas de la base de datos con los datos de las dos tablas pasadas como parámetro.
    
    :param db_filename: Fichero que se utilizará como BD
    :param tab_datos: Fichero csv con los datos generales de las empresas
    :param tab_ibex35: Fichero csv con los datos de cada empresa en el IBEX35
    :return: No devuelve nada
    """
    conn = crear_bd(db_filename)
    tab1 = lee_fichero_accidentes(tab_datos)
    tab2 = lee_fichero_accidentes(tab_ibex35)

    for fila1 in tab1:
        conn.execute("""
            INSERT INTO datos_generales (ticker, nombre, indice, pais) VALUES (?, ?, ?, ?)
        """
        , (fila1['ticker'], fila1['nombre'], fila1['indice'], fila1['pais']))

    for fila2 in tab2:
        fecha_transformada = transformar_fecha(fila2['fecha'])
        conn.execute("""
            INSERT INTO semanales_IBEX35 (ticker, fecha, precio) VALUES (?, ?, ?)
        """
        , (fila2['ticker'], fecha_transformada, fila2['precio']))

    conn.commit()
    conn.close()


def consulta1(db_filename, indice):
    """
    Consulta la base de datos para obtener el ticker y nombre de empresas 
    pertenecientes a un índice específico, ordenados por ticker en orden descendente.

    :param db_filename: Fichero que se utilizará como BD
    :param indice: Índice por el cual se filtran los datos
    :return: Un cursor con los resultados de la consulta
    """
    conn = crear_bd(db_filename)
    curr = conn.execute('''SELECT ticker, nombre
        FROM datos_generales
        WHERE indice = ?
        GROUP BY ticker
        ORDER BY ticker DESC''', [indice])
    conn.commit()
    conn.close()
    return curr

def consulta2(db_filename):
    """
    Consulta la base de datos para obtener el ticker, nombre y precio máximo de 
    todas las empresas del IBEX35, ordenados por nombre en orden ascendente.

    :param db_filename: Fichero que se utilizará como BD
    :return: Un cursor con los resultados de la consulta
    """
    conn = crear_bd(db_filename)
    curr = conn.execute('''SELECT d.ticker, d.nombre, MAX(s.precio) AS max_precio
                           FROM datos_generales d
                           JOIN semanales_IBEX35 s ON d.ticker = s.ticker
                           GROUP BY d.ticker, d.nombre
                           ORDER BY d.nombre ASC
                        ''')
    conn.commit()
    conn.close()
    return curr

def consulta3(db_filename, limite):
    """
    Consulta la base de datos para obtener el ticker, nombre, precio promedio y 
    diferencia entre el precio máximo y el precio mínimo de todas las empresas 
    que tienen un precio promedio mayor que el límite dado, ordenados por el 
    precio promedio en orden descendente.

    :param db_filename: Fichero que se utilizará como BD
    :param limite: Límite inferior del precio promedio para filtrar los datos
    :return: Un cursor con los resultados de la consulta
    """
    conn = crear_bd(db_filename)
    curr = conn.execute(''' SELECT d.ticker,
                                d.nombre, 
                                AVG(s.precio) AS precio_promedio, 
                                (MAX(s.precio) - MIN(s.precio)) AS diferencia
                            FROM datos_generales d
                            JOIN semanales_IBEX35 s ON d.ticker = s.ticker
                            GROUP BY d.ticker
                            HAVING precio_promedio > ?
                            ORDER BY precio_promedio DESC ''', [limite])
    conn.commit()
    conn.close()
    return curr



def consulta4(db_filename, ticker):
    """
    Consulta la base de datos para obtener el ticker, fecha y precio de todas 
    las semanas de una empresa concreta, ordenadas por fecha en orden descendente.

    :param db_filename: Fichero que se utilizará como BD
    :param ticker: ticker de la empresa a consultar
    :return: Un cursor con los resultados de la consulta
    """

    conn = crear_bd(db_filename)
    curr = conn.execute('''SELECT ticker,  date(fecha) AS fecha, precio
                           FROM semanales_IBEX35 
                           WHERE ticker = ?
                           ORDER BY fecha DESC
                        ''', [ticker])
    conn.commit()
    conn.close()
    return curr
