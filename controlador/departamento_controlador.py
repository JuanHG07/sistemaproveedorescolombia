from controlador.base_controlador import BaseControlador
from modelo.dao.departamento_dao import DepartamentoDAO
from modelo.dto.departamento import Departamento
from utilidades import validaciones as v
from utilidades.errores import ErrorNegocio


class DepartamentoControlador(BaseControlador):
    def __init__(self):
        self.dao = DepartamentoDAO()

    def listar(self):
        return self._leer(self.dao.listar)

    def crear(self, nombre):
        return self._escribir(
            lambda: self.dao.insertar(Departamento(nombre=v.texto(nombre, "nombre", 80))))

    def actualizar(self, id_departamento, nombre):
        def accion():
            self._debe_existir(self.dao.obtener_por_id(id_departamento), "El departamento")
            self.dao.actualizar(Departamento(id_departamento, v.texto(nombre, "nombre", 80)))
        self._escribir(accion)

    def eliminar(self, id_departamento):
        def accion():
            if self.dao.eliminar(id_departamento) == 0:
                raise ErrorNegocio("El departamento no existe o ya fue eliminado.")
        self._escribir(accion)