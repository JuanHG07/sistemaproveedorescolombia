from controlador import permisos
from modelo.dao.proveedor_producto_dao import ProveedorProductoDAO
from modelo.dto.proveedor_producto_dto import ProveedorProductoDTO
from utilidades import validaciones


class ProveedorProductoControlador:
    """Transacciones: que proveedor suministra que producto, a que precio y plazo."""

    def __init__(self):
        self.dao = ProveedorProductoDAO()

    def listar(self):
        return self.dao.listar_detallado()

    def asignar(self, id_proveedor, id_producto, precio, dias):
        permisos.exigir_escritura()
        dto = ProveedorProductoDTO(id_proveedor, id_producto,
                                   validaciones.numero_no_negativo(precio, "precio unitario"),
                                   int(validaciones.numero_no_negativo(dias, "dias de entrega")))
        return self.dao.insertar(dto)

    def actualizar(self, dto):
        permisos.exigir_escritura()
        return self.dao.actualizar(dto)

    def quitar(self, id_proveedor, id_producto):
        permisos.exigir_escritura()
        return self.dao.eliminar(id_proveedor, id_producto)
