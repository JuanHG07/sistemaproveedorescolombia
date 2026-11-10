from typing import List, Optional
from modelo.dao.base_dao import BaseDAO
from modelo.dto.tipo_usuario import TipoUsuario


class TipoUsuarioDAO(BaseDAO):
    _COLS = "id_tipo, nombre"

    def listar(self) -> List[TipoUsuario]:
        filas = self._consultar(f"SELECT {self._COLS} FROM tipo_usuario ORDER BY id_tipo")
        return [TipoUsuario(**f) for f in filas]

    def obtener_por_id(self, id_tipo: int) -> Optional[TipoUsuario]:
        fila = self._consultar_uno(
            f"SELECT {self._COLS} FROM tipo_usuario WHERE id_tipo = %s", (id_tipo,))
        return TipoUsuario(**fila) if fila else None

    def obtener_por_nombre(self, nombre: str) -> Optional[TipoUsuario]:
        fila = self._consultar_uno(
            f"SELECT {self._COLS} FROM tipo_usuario WHERE nombre = %s", (nombre,))
        return TipoUsuario(**fila) if fila else None
