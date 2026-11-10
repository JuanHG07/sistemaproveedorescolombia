from controlador.base_controlador import BaseControlador
from modelo.dao.ciudad_dao import CiudadDAO
from modelo.dto.ciudad import Ciudad
from utilidades import validaciones as v
from utilidades.errores import ErrorNegocio


class CiudadControlador(BaseControlador):
    def __init__(self):
        self.dao = CiudadDAO()

    def listar(self):
        return self._leer(self.dao.listar)

    def listar_por_departamento(self, id_departamento):
        """Alimenta el combo dependiente departamento -> ciudad."""
        return self._leer(lambda: self.dao.listar_por_departamento(
            v.entero_positivo(id_departamento, "departamento")))

    def crear(self, nombre, id_departamento):
        return self._escribir(lambda: self.dao.insertar(self._construir(None, nombre, id_departamento)))

    def actualizar(self, id_ciudad, nombre, id_departamento):
        def accion():
            self._debe_existir(self.dao.obtener_por_id(id_ciudad), "La ciudad")
            self.dao.actualizar(self._construir(id_ciudad, nombre, id_departamento))
        self._escribir(accion)

    def eliminar(self, id_ciudad):
        def accion():
            if self.dao.eliminar(id_ciudad) == 0:
                raise ErrorNegocio("La ciudad no existe o ya fue eliminada.")
        self._escribir(accion)

    @staticmethod
    def _construir(id_ciudad, nombre, id_departamento):
        return Ciudad(id_ciudad=id_ciudad,
                      nombre=v.texto(nombre, "nombre", 100),
                      id_departamento=v.entero_positivo(id_departamento, "departamento"))
