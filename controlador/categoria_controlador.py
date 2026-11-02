from controlador.base_controlador import BaseControlador
from modelo.dao.categoria_dao import CategoriaDAO
from modelo.dto.categoria import Categoria
from utilidades import validaciones as v
from utilidades.errores import ErrorNegocio


class CategoriaControlador(BaseControlador):
    def __init__(self):
        self.dao = CategoriaDAO()

    def listar(self):
        return self._leer(self.dao.listar)

    def obtener(self, id_categoria):
        return self._leer(lambda: self.dao.obtener_por_id(id_categoria))

    def crear(self, nombre, descripcion=""):
        return self._escribir(
            lambda: self.dao.insertar(self._construir(None, nombre, descripcion)))

    def actualizar(self, id_categoria, nombre, descripcion=""):
        def accion():
            self._debe_existir(self.dao.obtener_por_id(id_categoria), "La categoría")
            self.dao.actualizar(self._construir(id_categoria, nombre, descripcion))
        self._escribir(accion)

    def eliminar(self, id_categoria):
        def accion():
            if self.dao.eliminar(id_categoria) == 0:
                raise ErrorNegocio("La categoría no existe o ya fue eliminada.")
        self._escribir(accion)

    @staticmethod
    def _construir(id_categoria, nombre, descripcion):
        return Categoria(id_categoria=id_categoria,
                         nombre=v.texto(nombre, "nombre", 100),
                         descripcion=v.texto(descripcion, "descripción", 255, obligatorio=False))