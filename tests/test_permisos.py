import unittest
from controlador.sesion import Sesion
from controlador import permisos


class TestPermisos(unittest.TestCase):
    def test_esporadico_no_escribe(self):
        Sesion.tipo = "Esporadico"
        self.assertFalse(permisos.puede_escribir())
        self.assertTrue(permisos.puede_consultar())

    def test_tradicional_escribe_pero_no_admin(self):
        Sesion.tipo = "Tradicional"
        self.assertTrue(permisos.puede_escribir())
        self.assertFalse(permisos.es_admin())

    def test_admin(self):
        Sesion.tipo = "Administrador"
        self.assertTrue(permisos.es_admin())


if __name__ == "__main__":
    unittest.main()
