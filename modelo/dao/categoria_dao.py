from typing import List, Optional
from modelo.dao.base_dao import BaseDAO
from modelo.dto.categoria import Categoria


class CategoriaDAO(BaseDAO):
    _COLS = "id_categoria, nombre, descripcion"

    def insertar(self, c: Categoria) -> int:
        sql = "INSERT INTO categoria (nombre, descripcion) VALUES (%s, %s)"
        return self._insertar(sql, (c.nombre, c.descripcion))

    def listar(self) -> List[Categoria]:
        filas = self._consultar(f"SELECT {self._COLS} FROM categoria ORDER BY nombre")
        return [Categoria(**f) for f in filas]

    def obtener_por_id(self, id_categoria: int) -> Optional[Categoria]:
        fila = self._consultar_uno(
            f"SELECT {self._COLS} FROM categoria WHERE id_categoria = %s", (id_categoria,))
        return Categoria(**fila) if fila else None

    def actualizar(self, c: Categoria) -> int:
        sql = "UPDATE categoria SET nombre = %s, descripcion = %s WHERE id_categoria = %s"
        return self._ejecutar(sql, (c.nombre, c.descripcion, c.id_categoria))

    def eliminar(self, id_categoria: int) -> int:
        return self._ejecutar("DELETE FROM categoria WHERE id_categoria = %s", (id_categoria,))
