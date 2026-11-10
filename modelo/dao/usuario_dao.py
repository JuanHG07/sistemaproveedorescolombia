from typing import List, Optional
from modelo.dao.base_dao import BaseDAO
from modelo.dto.usuario import Usuario


class UsuarioDAO(BaseDAO):
    _COLS = "id_usuario, nombre_completo, username, password_hash, id_tipo, estado"

    def insertar(self, u: Usuario) -> int:
        sql = ("INSERT INTO usuario (nombre_completo, username, password_hash, id_tipo, estado) "
               "VALUES (%s, %s, %s, %s, %s)")
        return self._insertar(sql, (u.nombre_completo, u.username,
                                    u.password_hash, u.id_tipo, u.estado))

    def listar(self) -> List[Usuario]:
        filas = self._consultar(f"SELECT {self._COLS} FROM usuario ORDER BY nombre_completo")
        return [Usuario(**f) for f in filas]

    def obtener_por_id(self, id_usuario: int) -> Optional[Usuario]:
        fila = self._consultar_uno(
            f"SELECT {self._COLS} FROM usuario WHERE id_usuario = %s", (id_usuario,))
        return Usuario(**fila) if fila else None

    def obtener_por_username(self, username: str) -> Optional[Usuario]:
        fila = self._consultar_uno(
            f"SELECT {self._COLS} FROM usuario WHERE username = %s", (username,))
        return Usuario(**fila) if fila else None

    def contar_por_tipo(self, nombre_tipo: str) -> int:
        sql = ("SELECT COUNT(*) AS total FROM usuario u "
               "JOIN tipo_usuario t ON t.id_tipo = u.id_tipo WHERE t.nombre = %s")
        return self._consultar_uno(sql, (nombre_tipo,))["total"]

    def actualizar(self, u: Usuario) -> int:
        sql = ("UPDATE usuario SET nombre_completo = %s, username = %s, "
               "id_tipo = %s, estado = %s WHERE id_usuario = %s")
        return self._ejecutar(sql, (u.nombre_completo, u.username,
                                    u.id_tipo, u.estado, u.id_usuario))

    def actualizar_password(self, id_usuario: int, password_hash: str) -> int:
        return self._ejecutar("UPDATE usuario SET password_hash = %s WHERE id_usuario = %s",
                              (password_hash, id_usuario))

    def cambiar_estado(self, id_usuario: int, estado: str) -> int:
        return self._ejecutar("UPDATE usuario SET estado = %s WHERE id_usuario = %s",
                              (estado, id_usuario))

    def eliminar(self, id_usuario: int) -> int:
        return self._ejecutar("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
