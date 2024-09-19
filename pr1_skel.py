"""
TODO: rellenar

Asignatura: GIW
Práctica 1
Grupo: 05
Autores: Daniel Fernández Ortiz, Airam Martín Peraza, José Waldo Villacres Zumaeta

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""


# Ejercicio 1

def dimension(matriz):
    ...

def es_cuadrada(matriz):
    """
    Comprueba si una matriz es cuadrada.
    
    Parámetros:
    matriz (lista de listas): La matriz a comprobar.
    
    Returns:
    bool: True si la matriz es cuadrada, False en otro caso.
    """
    if (len(matriz) == 0 or len(matriz) == len(matriz[0])):
        return True

    return False

def es_simetrica(matriz):
    ...

def multiplica_escalar(matriz, k):
    ...

def suma(matriz1, matriz2):
    ...


# Ejercicio 2
def validar(grafo):
    ...

def grado_entrada(grafo, nodo):
    ...

def distancia(grafo, nodo):
    ...
   
