from typing import List, Optional
from modelo.dao.base_dao import BaseDAO
from modelo.dto.departamento import Departamento


class DepartamentoDAO(BaseDAO):
    _COLS = "id_departamento, nombre"

    def insertar(self, d: Departamento) -> int:
        return self._insertar("INSERT INTO departamento (nombre) VALUES (%s)", (d.nombre,))

    def listar(self) -> List[Departamento]:
        filas = self._consultar(f"SELECT {self._COLS} FROM departamento ORDER BY nombre")
        return [Departamento(**f) for f in filas]

    def obtener_por_id(self, id_departamento: int) -> Optional[Departamento]:
        fila = self._consultar_uno(
            f"SELECT {self._COLS} FROM departamento WHERE id_departamento = %s", (id_departamento,))
        return Departamento(**fila) if fila else None

    def actualizar(self, d: Departamento) -> int:
        return self._ejecutar("UPDATE departamento SET nombre = %s WHERE id_departamento = %s",
                              (d.nombre, d.id_departamento))

    def eliminar(self, id_departamento: int) -> int:
        return self._ejecutar("DELETE FROM departamento WHERE id_departamento = %s", (id_departamento,))