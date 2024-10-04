"""
TODO: rellenar

Asignatura: GIW
Práctica 1
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


# Ejercicio 1

def dimension(matriz):
    """
    Función que devuelve el número de filas y columnas de una matriz.

    Parámetros:
    matriz (lista de listas): La matriz a analizar.

    Returns:
    tuple: Un par (filas, columnas) si la matriz tiene tiene filas que son del mismo tamaño, 
                None en otro caso.
    """
    if not isinstance(matriz, list) or not matriz:
        return None

    filas = len(matriz)
    columnas = len(matriz[0])

    for fila in matriz[1:]:
        if len(fila) != columnas:
            return None

    return (filas, columnas)

def es_cuadrada(matriz):
    """
    Función que comprueba si una matriz es cuadrada.
    
    Parámetros:
    matriz (lista de listas): La matriz a comprobar.
    
    Returns:
    bool: True si la matriz es cuadrada, False en otro caso.
    """
    dim = dimension(matriz)

    if dim is None or not isinstance(matriz, list):
        return False

    return dim[0] == dim[1]

def es_simetrica(matriz):
    """
    Función que comprueba si una matriz es simétrica.

    Parámetros:
    matriz (lista de listas): La matriz a comprobar.

    Returns:
    bool: True si la matriz es simétrica, False en otro caso.
    """
    if es_cuadrada(matriz) is False:
        return False

    for fila, num_a in enumerate(matriz):
        for columna, _ in enumerate(num_a):
            if matriz[fila][columna] != matriz[columna][fila]:
                return False

    return True

def multiplica_escalar(matriz, k):
    """
    Función que devuelve la matriz multiplicada por un escalar k.
    
    Parámetros:
    matriz (lista de listas): La matriz a multiplicar.
    k (entero): El valor para multiplicar los elementos de la matriz
    
    Returns:
    matriz(lista de listas) | None: None si la matriz está mal construida, 
    la matriz multiplicada por el escalar en otro caso.
    """

    if es_cuadrada(matriz) is False or len(matriz) == 0:
        return None

    size = len(matriz[0])
    col = 0
    is_correct = True
    while col < len(matriz) and is_correct:
        if size != len(matriz[col]):
            is_correct = False
        col = col + 1

    if is_correct is False:
        return None

    matriz_multi = []
    for i in matriz:
        add_fila = []
        for j in i:
            add_fila.append(j * k)

        matriz_multi.append(add_fila)

    return matriz_multi

def suma(matriz1, matriz2):
    """
    Función que devuelve la suma de dos matrices.

    Parámetros:
    matriz1 (lista de listas): La primera matriz a sumar.
    matriz2 (lista de listas): La segunda matriz a sumar.

    Returns:
    lista de listas | None: La suma de las dos matrices, None si las matrices no pueden ser sumadas.
    """
    mat1 = dimension(matriz1)
    mat2 = dimension(matriz2)

    if mat1 is None or mat2 is None or mat1[0] != mat2[0] or mat1[1] != mat2[1] :
        return None

    matriz_resultado = [[0 for i in range(mat1[1])] for j in range(mat1[0])]
    for i in range(mat1[0]):
        for j in range(mat1[1]):
            matriz_resultado[i][j] = matriz1[i][j] + matriz2[i][j]

    return matriz_resultado


# Ejercicio 2
def validar(grafo):
    """
    Función que comprueba si un grafo está bien construido.
    
    Parámetros:
    grafo (diccionario): El grafo a validar. Debe contener las claves "nodos" y "aristas",
    siendo "nodos" una lista de nodos y "aristas" un diccionario en el cual 
    cada nodo tiene una lista de sus nodos adyacentes.
    
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
    """
    Función que devuelve el grado de entrada de un nodo en un grafo.

    Parámetros:
    grafo (diccionario): El grafo en el que puede estar o no el nodo.
    nodo (string): El nodo del que se quiere calcular el grado de entrada.

    Returns:
    int: El grado de entrada del nodo. Si el grafo no es válido o el nodo
    no existe en el grafo, se devuelve -1.
    """
    if validar(grafo) is False:
        return -1

    if nodo not in grafo["nodos"]:
        return -1

    cont = 0

    for _, b in grafo["aristas"].items():
        if nodo in b:
            cont += 1

    return cont

def distancia(grafo, nodo):
    """
    Función que devuelve la distancia mínima del nodo pasado por parámetro con el resto del grafo
    
    Parámetros:
    grafo (diccionario): El grafo en el que buscar las distancias mínimas entre los nodos
    nodo (string): El nodo del que se quiere saber la distancia mínima con el resto de nodos
    
    Returns:
    None | dict: 
    None si el grafo es inválido o si el nodo pasado por parámetro no existe en el grafo, 
    dict devuelve la distancia en forma de diccionario, en caso de que el nodo pasado por
    parámetro no pueda alcanzarlo se asigna -1 a dicho nodo no alcanzado.
    """

    if validar(grafo) is False:
        return None

    found = False
    i = 0
    while i < len(grafo['nodos']) and not found:
        if grafo['nodos'][i] == nodo:
            found = True
        else:
            i = i + 1

    if not found:
        return None

    distancias = dict() #Map<Nodo, Distancia> = Map<string, int>
    queue = []
    for n in grafo['nodos']: #Rellenamos el diccionario de distancias con -1,
        distancias[n] = -1  #en caso de no ser encontrado y también lo usaremos como marcaje

    distancias[nodo] = 0
    queue.append(nodo)
    while len(queue) != 0: #Algoritmo de Recorrido en Anchura
        v = queue[0]
        queue.pop(0)
        for w in grafo["aristas"][v]:
            if distancias[w] == -1:
                dist = 0
                if distancias[v] != -1:
                    dist = distancias[v]
                distancias[w] = dist + 1
                queue.append(w)

    return distancias
