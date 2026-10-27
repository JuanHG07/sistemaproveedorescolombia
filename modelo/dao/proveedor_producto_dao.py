from modelo.dao.base_dao import BaseDAO
from modelo.dto.proveedor_producto_dto import ProveedorProductoDTO


class ProveedorProductoDAO(BaseDAO):
    """SQL de la tabla asociativa proveedor_producto (N:M)."""

    def insertar(self, dto):
        sql = ("INSERT INTO proveedor_producto "
               "(id_proveedor, id_producto, precio_unitario, dias_entrega) "
               "VALUES (%s, %s, %s, %s)")
        return self.ejecutar(sql, (dto.id_proveedor, dto.id_producto,
                                   dto.precio_unitario, dto.dias_entrega))

    def listar_detallado(self):
        sql = ("SELECT pp.id_proveedor, pp.id_producto, pr.razon_social, "
               "p.codigo, p.nombre AS producto, pp.precio_unitario, pp.dias_entrega "
               "FROM proveedor_producto pp "
               "JOIN proveedor pr ON pr.id_proveedor = pp.id_proveedor "
               "JOIN producto p ON p.id_producto = pp.id_producto "
               "ORDER BY pr.razon_social, p.nombre")
        return self.consultar(sql)

    def actualizar(self, dto):
        sql = ("UPDATE proveedor_producto SET precio_unitario = %s, dias_entrega = %s "
               "WHERE id_proveedor = %s AND id_producto = %s")
        return self.ejecutar(sql, (dto.precio_unitario, dto.dias_entrega,
                                   dto.id_proveedor, dto.id_producto))

    def eliminar(self, id_proveedor, id_producto):
        return self.ejecutar(
            "DELETE FROM proveedor_producto WHERE id_proveedor = %s AND id_producto = %s",
            (id_proveedor, id_producto))
