from typing import List, Optional
from modelo.dao.base_dao import BaseDAO
from modelo.dto.proveedor_producto import ProveedorProducto


class ProveedorProductoDAO(BaseDAO):
    _COLS = "id_proveedor, id_producto, precio_unitario, dias_entrega"

    def insertar(self, pp: ProveedorProducto) -> int:
        sql = ("INSERT INTO proveedor_producto (id_proveedor, id_producto, precio_unitario, dias_entrega) "
               "VALUES (%s, %s, %s, %s)")
        return self._ejecutar(sql, (pp.id_proveedor, pp.id_producto,
                                    pp.precio_unitario, pp.dias_entrega))

    def listar(self) -> List[ProveedorProducto]:
        filas = self._consultar(f"SELECT {self._COLS} FROM proveedor_producto")
        return [ProveedorProducto(**f) for f in filas]

    def listar_por_proveedor(self, id_proveedor: int) -> List[ProveedorProducto]:
        filas = self._consultar(
            f"SELECT {self._COLS} FROM proveedor_producto WHERE id_proveedor = %s", (id_proveedor,))
        return [ProveedorProducto(**f) for f in filas]

    def listar_por_producto(self, id_producto: int) -> List[ProveedorProducto]:
        filas = self._consultar(
            f"SELECT {self._COLS} FROM proveedor_producto WHERE id_producto = %s", (id_producto,))
        return [ProveedorProducto(**f) for f in filas]

    def obtener(self, id_proveedor: int, id_producto: int) -> Optional[ProveedorProducto]:
        fila = self._consultar_uno(
            f"SELECT {self._COLS} FROM proveedor_producto "
            "WHERE id_proveedor = %s AND id_producto = %s", (id_proveedor, id_producto))
        return ProveedorProducto(**fila) if fila else None

    def actualizar(self, pp: ProveedorProducto) -> int:
        sql = ("UPDATE proveedor_producto SET precio_unitario = %s, dias_entrega = %s "
               "WHERE id_proveedor = %s AND id_producto = %s")
        return self._ejecutar(sql, (pp.precio_unitario, pp.dias_entrega,
                                    pp.id_proveedor, pp.id_producto))

    def eliminar(self, id_proveedor: int, id_producto: int) -> int:
        return self._ejecutar(
            "DELETE FROM proveedor_producto WHERE id_proveedor = %s AND id_producto = %s",
            (id_proveedor, id_producto))

    def listar_detallado(self) -> list:
        sql = ("SELECT pp.id_proveedor, pp.id_producto, pr.razon_social AS proveedor, "
               "p.codigo, p.nombre AS producto, pp.precio_unitario, pp.dias_entrega "
               "FROM proveedor_producto pp "
               "JOIN proveedor pr ON pr.id_proveedor = pp.id_proveedor "
               "JOIN producto p ON p.id_producto = pp.id_producto "
               "ORDER BY pr.razon_social, p.nombre")
        return self._consultar(sql)
