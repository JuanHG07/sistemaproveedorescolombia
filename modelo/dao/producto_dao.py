from typing import List, Optional
from modelo.dao.base_dao import BaseDAO
from modelo.dto.producto import Producto


class ProductoDAO(BaseDAO):
    _COLS = "id_producto, codigo, nombre, descripcion, unidad_medida, id_categoria, estado"

    def insertar(self, p: Producto) -> int:
        sql = ("INSERT INTO producto (codigo, nombre, descripcion, unidad_medida, id_categoria, estado) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
        return self._insertar(sql, (p.codigo, p.nombre, p.descripcion,
                                    p.unidad_medida, p.id_categoria, p.estado))

    def listar(self) -> List[Producto]:
        filas = self._consultar(f"SELECT {self._COLS} FROM producto ORDER BY nombre")
        return [Producto(**f) for f in filas]

    def listar_por_categoria(self, id_categoria: int) -> List[Producto]:
        filas = self._consultar(
            f"SELECT {self._COLS} FROM producto WHERE id_categoria = %s ORDER BY nombre",
            (id_categoria,))
        return [Producto(**f) for f in filas]

    def obtener_por_id(self, id_producto: int) -> Optional[Producto]:
        fila = self._consultar_uno(
            f"SELECT {self._COLS} FROM producto WHERE id_producto = %s", (id_producto,))
        return Producto(**fila) if fila else None

    def obtener_por_codigo(self, codigo: str) -> Optional[Producto]:
        fila = self._consultar_uno(
            f"SELECT {self._COLS} FROM producto WHERE codigo = %s", (codigo,))
        return Producto(**fila) if fila else None

    def actualizar(self, p: Producto) -> int:
        sql = ("UPDATE producto SET codigo = %s, nombre = %s, descripcion = %s, "
               "unidad_medida = %s, id_categoria = %s, estado = %s WHERE id_producto = %s")
        return self._ejecutar(sql, (p.codigo, p.nombre, p.descripcion, p.unidad_medida,
                                    p.id_categoria, p.estado, p.id_producto))

    def cambiar_estado(self, id_producto: int, estado: str) -> int:
        return self._ejecutar("UPDATE producto SET estado = %s WHERE id_producto = %s",
                              (estado, id_producto))

    def eliminar(self, id_producto: int) -> int:
        return self._ejecutar("DELETE FROM producto WHERE id_producto = %s", (id_producto,))
