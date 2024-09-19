import unittest
import pr1_skel as pr1

class TestEsCuadrada(unittest.TestCase):
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
        self.assertEqual(pr1.es_cuadrada([]), True)
    
if __name__ == '__main__':
    unittest.main()