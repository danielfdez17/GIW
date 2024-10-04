import unittest
import pr2
from pprint import pprint

class TestLeerFicheroAccidentes(unittest.TestCase):
    """
    """

    def test_leer_fichero_accidentes(self):
        self.assertIsNotNone(pr2.lee_fichero_accidentes("./practica2/AccidentesBicicletas_2021.csv"))


    def test_mostrar_lista_fichero_accidentes(self):
        pprint(pr2.lee_fichero_accidentes("./practica2/AccidentesBicicletas_2021.csv"))


class TestPuntosNegros(unittest.TestCase):
    def test_leer_fichero_accidentes(self):
        self.assertEquals(pr2.puntos_negros_distrito(pr2.lee_fichero_accidentes("./practica2/AccidentesBicicletas_2021.csv"), "MONCLOA-ARAVACA", 16), 
                          [('PASEO. PIÑONERO, 4', 3),
                            ('CTRA. PARQUE DE ATRACCIONES, 1', 3),
                            ('CTRA. CIUDAD UNIVERSITARIA, 0', 3),
                            ('PASEO. TORRECILLA / PASEO. AZUL', 2),
                            ('PASEO. REY, 22', 2),
                            ('PASEO. EMBARCADERO, 6', 2),
                            ('PASEO. EMBARCADERO / PASEO. AZUL', 2),
                            ('PASEO. AZUL / PASEO. EMBARCADERO', 2),
                            ('PASEO PIÑONEROS KM 46,708 VIA VERDE CASA DE CAMPO', 2),
                            ('CUSTA. SAN VICENTE, 44', 2),
                            ('CTRA. GARABITAS, 0', 2),
                            ('CTRA. CASTILLA, +00100S', 2),
                            ('CALL. JOSE ANTONIO NOVAIS / CALL. RAMIRO DE MAEZTU', 2),
                            ('CALL. IRUN, 1', 2),
                            ('CALL. ANICETO MARINAS, 74', 2),
                            ('AVDA. COMPLUTENSE, 14', 2)])


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