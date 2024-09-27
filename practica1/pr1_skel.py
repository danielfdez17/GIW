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
    """
    Devolvemos una matriz a partir de multiplicar los elementos de la matriz original por el valor k
    
    Parámetros:
    matriz (lista de listas): La matriz a multiplicar.
    k (entero): El valor para multiplicar los elementos de la matriz
    
    Returns:
    matriz(lista de listas) | None: None en caso de que la matriz este mal construida, devuelve la matriz multiplicada en caso de que es bien construida.
    """

    if len(matriz) == 0: 
        return None
    
    size = len(matriz[0])
    col = 0
    is_correct = True
    while col < len(matriz) and is_correct:
        if size != len(matriz[col]):
            is_correct = False
        col = col + 1

    if is_correct == False:
        return None
    
    matriz_multi = []
    for i in range(len(matriz)):
        add_fila = []
        for j in range(size):
            add_fila.append(matriz[i][j] * k)
        
        matriz_multi.append(add_fila)
         
    return matriz_multi
        

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
    """
    Encuentra la distancia minima del nodo pasado por parametro con el resto del grafo
    
    Parámetros:
    grafo (diccionario): El grafo a buscar las distancia minima entre los nodos
    nodo (string): El nodo a buscar la distancia minima con el resto de nodos
    
    Returns:
    None | dict: None si el grafo es invalido o si el nodo pasado por parametro no existe en el grafo, 
                 dict devuelve la distancia en forma de diccionario, en caso de que el nodo pasado por
                 parametro no pueda alcanzarlo devolveremos -1 en el mapa.
    """

    if validar(grafo) == False: #Comprobamos si el grafo es valido
        return None
    
    found = False
    i = 0
    while i < len(grafo['nodos']) and not found: #Comprobamos que exista el nodo en el grafo
        if grafo['nodos'][i] == nodo:
            found = True
        else:
            i = i + 1

    if not found:
        return None 
    
    distancias = dict() #Map<Nodo, Distanca> = Map<string, int>
    queue = []
    for n in grafo['nodos']:#Rellenamos el diccionario de distancias con -1,
        distancias[n] = -1  #en caso de no ser encontrado y tambien lo usaremos como marcaje
    
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
