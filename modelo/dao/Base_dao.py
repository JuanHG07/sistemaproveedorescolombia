from mysql.connector import Error
from database.conexion import Conexion


class BaseDAO:
    def _consultar(self, sql, params=()):
        con = Conexion.obtener()
        cursor = con.cursor(dictionary=True)
        try:
            cursor.execute(sql, params)
            filas = cursor.fetchall()
            con.commit() 
            return filas
        finally:
            cursor.close()

    def _consultar_uno(self, sql, params=()):
        filas = self._consultar(sql, params)
        return filas[0] if filas else None

    def _escribir(self, sql, params, devolver_id):
        con = Conexion.obtener()
        cursor = con.cursor()
        try:
            cursor.execute(sql, params)
            con.commit()
            return cursor.lastrowid if devolver_id else cursor.rowcount
        except Error:
            con.rollback()
            raise
        finally:
            cursor.close()

    def _insertar(self, sql, params=()):
        return self._escribir(sql, params, devolver_id=True)

    def _ejecutar(self, sql, params=()):
        return self._escribir(sql, params, devolver_id=False)