from typing import List, Optional
from modelo.dao.base_dao import BaseDAO
from modelo.dto.ciudad import Ciudad


class CiudadDAO(BaseDAO):
    _COLS = "id_ciudad, nombre, id_departamento"

    def insertar(self, c: Ciudad) -> int:
        sql = "INSERT INTO ciudad (nombre, id_departamento) VALUES (%s, %s)"
        return self._insertar(sql, (c.nombre, c.id_departamento))

    def listar(self) -> List[Ciudad]:
        filas = self._consultar(f"SELECT {self._COLS} FROM ciudad ORDER BY nombre")
        return [Ciudad(**f) for f in filas]

    def listar_por_departamento(self, id_departamento: int) -> List[Ciudad]:
        filas = self._consultar(
            f"SELECT {self._COLS} FROM ciudad WHERE id_departamento = %s ORDER BY nombre",
            (id_departamento,))
        return [Ciudad(**f) for f in filas]

    def obtener_por_id(self, id_ciudad: int) -> Optional[Ciudad]:
        fila = self._consultar_uno(
            f"SELECT {self._COLS} FROM ciudad WHERE id_ciudad = %s", (id_ciudad,))
        return Ciudad(**fila) if fila else None

    def actualizar(self, c: Ciudad) -> int:
        sql = "UPDATE ciudad SET nombre = %s, id_departamento = %s WHERE id_ciudad = %s"
        return self._ejecutar(sql, (c.nombre, c.id_departamento, c.id_ciudad))

    def eliminar(self, id_ciudad: int) -> int:
        return self._ejecutar("DELETE FROM ciudad WHERE id_ciudad = %s", (id_ciudad,))
