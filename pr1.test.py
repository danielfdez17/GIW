import unittest
import pr1_skel as pr1

class TestEsCuadrada(unittest.TestCase):
    """
    Clase para probar la función es_cuadrada(matriz)
    """
    def test_es_cuadrada_ok(self):
        """
        Comprueba que una matriz cuadrada sea detectada correctamente.
        """
        self.assertEqual(pr1.es_cuadrada([[1, 2], [3, 4]]), True)

    def test_es_cuadrada_ko(self):
        """
        Comprueba que una matriz no cuadrada no sea detectada como tal.
        """
        self.assertEqual(pr1.es_cuadrada([[1, 2], [3, 4], [5, 6]]), False)

    def test_es_cuadrada_ko2(self):
        """
        Comprueba que una matriz vac a sea detectada como cuadrada.
        """
        self.assertEqual(pr1.es_cuadrada([]), True)


class TestMultiplicarEscalar(unittest.TestCase):
    """
    Clase para probar la función multiplica_escalar(matriz, k)
    """

    """
    Comprueba si la matriz es vacia
    """
    def test_check_empty_matriz(self):
        self.assertIsNone(pr1.multiplica_escalar([], 2))

    """
    Comprueba si la matriz esta bien construida, es decir que las filas tienen el mismo tamanio
    """
    def test_check_is_not_build_good_matriz(self):
        self.assertIsNone(pr1.multiplica_escalar([ 
                                                  [1], 
                                                  [1, 2]], 2))
    
    """
    Comprueba si la matriz no es vacia
    """
    def test_check_not_empty_matriz(self):
        self.assertIsNotNone(pr1.multiplica_escalar([ [2, 0, 2], 
                                                      [0, 6, 4], 
                                                      [2, 4, 4]], 2))

    """
    Comprueba si la matriz es multiplicada correctamente por la constante k
    """
    def test_check_multiplica_escalar(self):
        self.assertEqual(pr1.multiplica_escalar([ [2, 0, 2], 
                                                    [0, 6, 4], 
                                                    [2, 4, 4]], 2), [[4, 0, 4], [0, 12, 8],[4, 8, 8]])

class TestValidar(unittest.TestCase):
    """
    Clase para probar la función validar(grafo)
    """
    grafo_valido = {
        "nodos": ["a", "b", "c", "d"],
        "aristas": {
            "a": ["a", "b", "c"],
            "b": ["a", "c"],
            "c": ["c"],
            "d": ["c"]
        }
    }
    grafo_con_mas_claves = {
        "nodos": [],
        "aristas" : {},
        "errores": "muchos"
    }
    grafo_con_menos_claves = {
        "nodos": [1, 2, 3, 4],
    }
    grafo_con_claves_incorrectas = {
        "errores": "muchos"
    }
    grafo_vacio = {}
    grafo_con_lista_de_nodos_vacias = {
        "nodos": [],
    }
    grafo_con_nodos_repetidos = {
        "nodos": ["a", "b", "a"],
    }
    grafo_con_nodos_origen_no_definidos_en_nodos = {
        "nodos": [1, 2, 3],
        "aristas": {
            1: [2, 3, 4],
            4: [3],
        }
    }
    grafo_con_nodos_destino_no_definidos_en_nodos = {
        "nodos": [1, 2, 3],
        "aristas": {
            1: [2, 3, 4],
        }
    }
    grafo_con_nodos_destino_repetidos = {
        "nodos": [1, 2, 3],
        "aristas": {
            1: [2, 3, 2],
        }
    }

    def test_validar_ok(self):
        """
        Comprueba que un grafo que cumpla con las condiciones sea detectado como v lido.
        """
        self.assertEqual(pr1.validar(self.grafo_valido), True)


    def test_validar_ko(self):
        """
        Comprueba que un grafo que no cumpla con las condiciones no sea detectado como v lido.
        """
        self.assertEqual(pr1.validar(self.grafo_con_mas_claves), False)
        self.assertEqual(pr1.validar(self.grafo_con_menos_claves), False)
        self.assertEqual(pr1.validar(self.grafo_con_claves_incorrectas), False)
        self.assertEqual(pr1.validar(self.grafo_vacio), False)
        self.assertEqual(pr1.validar(self.grafo_con_lista_de_nodos_vacias), False)
        self.assertEqual(pr1.validar(self.grafo_con_nodos_repetidos), False)
        self.assertEqual(pr1.validar(self.grafo_con_nodos_origen_no_definidos_en_nodos), False)
        self.assertEqual(pr1.validar(self.grafo_con_nodos_destino_no_definidos_en_nodos), False)
        self.assertEqual(pr1.validar(self.grafo_con_nodos_destino_repetidos), False)


if __name__ == '__main__':
    unittest.main()
