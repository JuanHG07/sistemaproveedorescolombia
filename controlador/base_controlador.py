from mysql.connector import Error
from controlador import permisos
from utilidades.errores import ErrorNegocio, traducir_error


class BaseControlador:

    @staticmethod
    def _proteger(accion):
        try:
            return accion()
        except Error as e:
            raise ErrorNegocio(traducir_error(e))
        except ConnectionError as e:
            raise ErrorNegocio(str(e))

    def _leer(self, accion):
        permisos.exigir_sesion()
        return self._proteger(accion)

    def _escribir(self, accion):
        permisos.exigir_escritura()
        return self._proteger(accion)

    def _como_admin(self, accion):
        permisos.exigir_admin()
        return self._proteger(accion)

    @staticmethod
    def _debe_existir(objeto, nombre):
        if objeto is None:
            raise ErrorNegocio(f"{nombre} no existe.")
