import unittest
import pr2_skel as pr2
from pprint import pprint

class TestLeerFicheroAccidentes(unittest.TestCase):
    """
    """

    def test_leer_fichero_accidentes(self):
        self.assertIsNotNone(pr2.lee_fichero_accidentes("./practica2/AccidentesBicicletas_2021.csv"))


    def test_mostrar_lista_fichero_accidentes(self):
        pprint(pr2.lee_fichero_accidentes("./practica2/AccidentesBicicletas_2021.csv"))


class TestLeerMonumentos(unittest.TestCase):
    def test_leer_monumento(self):
        self.assertGreater(len(pr2.leer_monumentos("./practica2/300356-0-monumentos-ciudad-madrid.json")), 0)


class TestBusquedaDistancia(unittest.TestCase):
    def test_leer_fichero_accidentes(self):
        self.assertEquals(pr2.busqueda_distancia(pr2.leer_monumentos("./practica2/300356-0-monumentos-ciudad-madrid.json"), "Profesor José García Santesmases 9, Madrid, España", 1), [('José Ortega y Gasset', '400073', 0.3759164404192351),
                                                                                                                                                                                        ('Camilo José Cela', '408914', 0.46455683243115004),
                                                                                                                                                                                        ('Alfonso XIII', '400063', 0.6612413986049323),
                                                                                                                                                                                        ('Puerta de Hierro', '400408', 0.9218447173625832),
                                                                                                                                                                                        ('Blas Lázaro e Ibiza', '409134', 0.9949662127532939)])
if __name__ == '__main__':
    unittest.main()