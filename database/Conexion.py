import mysql.connector
from mysql.connector import Error


class Conexion:
    CONFIG = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "tu_clave",
        "database": "proveedores_db",
    }

    _conexion = None  

    @classmethod
    def obtener(cls):
        try:
            if cls._conexion is None or not cls._conexion.is_connected():
                cls._conexion = mysql.connector.connect(**cls.CONFIG)
            return cls._conexion
        except Error as e:
            raise ConnectionError(f"No se pudo conectar a MySQL: {e}")

    @classmethod
    def cerrar(cls):
        if cls._conexion is not None and cls._conexion.is_connected():
            cls._conexion.close()
        cls._conexion = None