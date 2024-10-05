import unittest
import pr3

"""
    TODO: Preguntar al profe si es necesario validar que exista el fichero y si el xml
    es un fichero valido con Exception.
"""
class TestBusquedaCercania(unittest.TestCase):
    def test_busqueda_cercania(self):
        self.assertGreater(len(pr3.busqueda_cercania("./practica3/restaurantes_v1_es.xml", "Profesor José García Santesmases 9, Madrid, España", 3)), 0)


    def test_busqueda_cercania_empty_lugar(self):
        self.assertEqual(len(pr3.busqueda_cercania("./practica3/restaurantes_v1_es.xml", "", 3)), 0,  "La funcion deberia devolver una lista vacia cuando se proporciona una ubicacion vacia o que no exista")
    

    def test_busqueda_cercania_file_dont_found(self):
        self.assertEqual(len(pr3.busqueda_cercania("./practica3/luis.xml", "", 3)), 0)


if __name__ == '__main__':
    unittest.main()
