import unittest
import pr2_skel as pr2
from pprint import pprint



class TestLeerFicheroAccidentes(unittest.TestCase):
    """
    """

    def test_leer_fichero_accidentes(self):
        self.assertIsNotNone(pr2.lee_fichero_accidentes("AccidentesBicicletas_2021.csv"))


    def test_mostrar_lista_fichero_accidentes(self):
        pprint(pr2.lee_fichero_accidentes("AccidentesBicicletas_2021.csv"))


class TestBusquedaDistancia(unittest.TestCase):
       def test_leer_fichero_accidentes(self):
        self.assertEquals(pr2.busqueda_distancia("Profesor José García Santesmases 9, Madrid, España", 1))
