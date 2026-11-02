from controlador.base_controlador import BaseControlador
from modelo.dao.producto_dao import ProductoDAO
from modelo.dto.producto import Producto
from utilidades import validaciones as v
from utilidades.constantes import ACTIVO
from utilidades.errores import ErrorNegocio


class ProductoControlador(BaseControlador):
    def __init__(self):
        self.dao = ProductoDAO()

    def listar(self):
        return self._leer(self.dao.listar)

    def listar_por_categoria(self, id_categoria):
        return self._leer(lambda: self.dao.listar_por_categoria(
            v.entero_positivo(id_categoria, "categoría")))

    def obtener(self, id_producto):
        return self._leer(lambda: self.dao.obtener_por_id(id_producto))

    def crear(self, codigo, nombre, descripcion, unidad_medida, id_categoria, estado=ACTIVO):
        return self._escribir(lambda: self.dao.insertar(self._construir(
            None, codigo, nombre, descripcion, unidad_medida, id_categoria, estado)))

    def actualizar(self, id_producto, codigo, nombre, descripcion,
                   unidad_medida, id_categoria, estado):
        def accion():
            self._debe_existir(self.dao.obtener_por_id(id_producto), "El producto")
            self.dao.actualizar(self._construir(
                id_producto, codigo, nombre, descripcion, unidad_medida, id_categoria, estado))
        self._escribir(accion)

    def cambiar_estado(self, id_producto, estado):
        self._escribir(lambda: self.dao.cambiar_estado(id_producto, v.estado(estado)))

    def eliminar(self, id_producto):
        def accion():
            if self.dao.eliminar(id_producto) == 0:
                raise ErrorNegocio("El producto no existe o ya fue eliminado.")
        self._escribir(accion)

    @staticmethod
    def _construir(id_producto, codigo, nombre, descripcion, unidad_medida, id_categoria, estado):
        return Producto(
            id_producto=id_producto,
            codigo=v.texto(codigo, "código", 30),
            nombre=v.texto(nombre, "nombre", 150),
            descripcion=v.texto(descripcion, "descripción", 255, obligatorio=False),
            unidad_medida=v.texto(unidad_medida, "unidad de medida", 30),
            id_categoria=v.entero_positivo(id_categoria, "categoría"),
            estado=v.estado(estado))