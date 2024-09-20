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
    # Diccionario contiene exactamente las claves "nodos" y "aristas"
    """
    Valida si un grafo cumple con ciertas condiciones.
    
    Parámetros:
    grafo (diccionario): El grafo a validar. Debe contener las claves "nodos" y "aristas",
    siendo "nodos" una lista de nodos y "aristas" un diccionario que a cada nodo le
    asigna una lista de sus nodos vecinos.
    
    Returns:
    bool: True si el grafo es válido, False en caso contrario.
    """

    # El diccionario contiene exactamente las claves 'nodos' y 'aristas'
    if len(grafo) != 2 or 'nodos' not in grafo or 'aristas' not in grafo:
        return False

    # La lista de nodos es no vacía
    if len(grafo['aristas']) == 0:
        return False

    # 'nodos' no tiene nodos repetidos
    for nodo in grafo['nodos']:
        if grafo['nodos'].count(nodo) > 1:
            return False

    # Los nodos origen que aparecen en aristas son exactamente los nodos definidos en 'nodos'
    for nodo in grafo['aristas']:
        if nodo not in grafo['nodos']:
            return False

    # Los nodos destino que aparecen en aristas están definidos en nodos y no están repetidos
    for nodo in grafo['aristas']:
        set_nodos_destino = set()
        for destino in grafo['aristas'][nodo]:
            if destino not in grafo['nodos'] or destino in set_nodos_destino:
                return False
            set_nodos_destino.add(destino)

    return True

def grado_entrada(grafo, nodo):
    ...

def distancia(grafo, nodo):
    ...
