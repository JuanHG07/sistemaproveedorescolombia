from controlador.base_controlador import BaseControlador
from modelo.dao.proveedor_producto_dao import ProveedorProductoDAO
from modelo.dto.proveedor_producto import ProveedorProducto
from utilidades import validaciones as v
from utilidades.errores import ErrorNegocio


class ProveedorProductoControlador(BaseControlador):

    def __init__(self):
        self.dao = ProveedorProductoDAO()

    def listar_detallado(self):
        return self._leer(self.dao.listar_detallado)

    def listar_por_proveedor(self, id_proveedor):
        return self._leer(lambda: self.dao.listar_por_proveedor(
            v.entero_positivo(id_proveedor, "proveedor")))

    def listar_por_producto(self, id_producto):
        return self._leer(lambda: self.dao.listar_por_producto(
            v.entero_positivo(id_producto, "producto")))

    def asignar(self, id_proveedor, id_producto, precio_unitario, dias_entrega):
        def accion():
            pp = self._construir(id_proveedor, id_producto, precio_unitario, dias_entrega)
            if self.dao.obtener(pp.id_proveedor, pp.id_producto) is not None:
                raise ErrorNegocio("Ese proveedor ya suministra ese producto. "
                                   "Edite el precio o los días de entrega.")
            self.dao.insertar(pp)
        self._escribir(accion)

    def actualizar(self, id_proveedor, id_producto, precio_unitario, dias_entrega):
        def accion():
            pp = self._construir(id_proveedor, id_producto, precio_unitario, dias_entrega)
            self._debe_existir(self.dao.obtener(pp.id_proveedor, pp.id_producto), "La relación")
            self.dao.actualizar(pp)
        self._escribir(accion)

    def quitar(self, id_proveedor, id_producto):
        def accion():
            if self.dao.eliminar(v.entero_positivo(id_proveedor, "proveedor"),
                                 v.entero_positivo(id_producto, "producto")) == 0:
                raise ErrorNegocio("La relación no existe o ya fue eliminada.")
        self._escribir(accion)

    @staticmethod
    def _construir(id_proveedor, id_producto, precio_unitario, dias_entrega):
        return ProveedorProducto(
            id_proveedor=v.entero_positivo(id_proveedor, "proveedor"),
            id_producto=v.entero_positivo(id_producto, "producto"),
            precio_unitario=v.numero_no_negativo(precio_unitario, "precio unitario"),
            dias_entrega=v.entero_no_negativo(dias_entrega, "días de entrega"))