import mysql.connector
from config.settings import DB_CONFIG


class Conexion:
    """Conexion unica y reutilizable a MySQL."""
    _con = None

    @classmethod
    def obtener(cls):
        if cls._con is None or not cls._con.is_connected():
            cls._con = mysql.connector.connect(**DB_CONFIG)
        return cls._con

    @classmethod
    def cerrar(cls):
        if cls._con is not None and cls._con.is_connected():
            cls._con.close()
        cls._con = None
