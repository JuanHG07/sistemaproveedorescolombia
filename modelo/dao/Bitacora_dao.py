from typing import List
from modelo.dao.base_dao import BaseDAO
from modelo.dto.bitacora import Bitacora


class BitacoraDAO(BaseDAO):
    _COLS = "id_bitacora, id_usuario, fecha_hora_entrada, fecha_hora_salida"

    def registrar_entrada(self, id_usuario: int) -> int:
        sql = "INSERT INTO bitacora (id_usuario, fecha_hora_entrada) VALUES (%s, NOW())"
        return self._insertar(sql, (id_usuario,))

    def registrar_salida(self, id_bitacora: int) -> int:
        sql = ("UPDATE bitacora SET fecha_hora_salida = NOW() "
               "WHERE id_bitacora = %s AND fecha_hora_salida IS NULL")
        return self._ejecutar(sql, (id_bitacora,))

    def listar(self) -> List[Bitacora]:
        filas = self._consultar(
            f"SELECT {self._COLS} FROM bitacora ORDER BY fecha_hora_entrada DESC")
        return [Bitacora(**f) for f in filas]

    def listar_por_usuario(self, id_usuario: int) -> List[Bitacora]:
        filas = self._consultar(
            f"SELECT {self._COLS} FROM bitacora WHERE id_usuario = %s "
            "ORDER BY fecha_hora_entrada DESC", (id_usuario,))
        return [Bitacora(**f) for f in filas]

    def listar_detallado(self) -> list:
        sql = ("SELECT b.id_bitacora, u.username, u.nombre_completo, t.nombre AS tipo, "
               "b.fecha_hora_entrada, b.fecha_hora_salida "
               "FROM bitacora b "
               "JOIN usuario u ON u.id_usuario = b.id_usuario "
               "JOIN tipo_usuario t ON t.id_tipo = u.id_tipo "
               "ORDER BY b.fecha_hora_entrada DESC")
        return self._consultar(sql)