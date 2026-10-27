from database.conexion import Conexion


class BaseDAO:
    """Metodos comunes. Siempre consultas parametrizadas (%s)."""

    def consultar(self, sql, params=None):
        """SELECT -> lista de diccionarios."""
        con = Conexion.obtener()
        cur = con.cursor(dictionary=True)
        try:
            cur.execute(sql, params or ())
            return cur.fetchall()
        finally:
            cur.close()

    def ejecutar(self, sql, params=None):
        """INSERT/UPDATE/DELETE -> lastrowid (insert) o filas afectadas."""
        con = Conexion.obtener()
        cur = con.cursor()
        try:
            cur.execute(sql, params or ())
            con.commit()
            return cur.lastrowid if cur.lastrowid else cur.rowcount
        except Exception:
            con.rollback()
            raise
        finally:
            cur.close()
