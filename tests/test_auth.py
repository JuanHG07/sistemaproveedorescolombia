import unittest
from utilidades import seguridad


class TestSeguridad(unittest.TestCase):
    def test_hash_y_verificacion(self):
        h = seguridad.hashear("Clave123")
        self.assertTrue(seguridad.verificar("Clave123", h))
        self.assertFalse(seguridad.verificar("otra", h))


if __name__ == "__main__":
    unittest.main()
