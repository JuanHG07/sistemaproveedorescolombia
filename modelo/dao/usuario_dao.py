from modelo.dao.base_dao import BaseDAO
from modelo.dto.usuario_dto import UsuarioDTO


class UsuarioDAO(BaseDAO):
    """Todo el SQL de la tabla usuario."""

    def insertar(self, dto):
        sql = "INSERT INTO usuario (nombre_completo, username, password_hash, id_tipo, estado) VALUES (%s, %s, %s, %s, %s)"
        return self.ejecutar(sql, (dto.nombre_completo, dto.username, dto.password_hash, dto.id_tipo, dto.estado,))

    def listar(self):
        return [UsuarioDTO(**f) for f in self.consultar("SELECT * FROM usuario")]

    def obtener(self, id_):
        filas = self.consultar("SELECT * FROM usuario WHERE id_usuario = %s", (id_,))
        return UsuarioDTO(**filas[0]) if filas else None

    def actualizar(self, dto):
        sql = "UPDATE usuario SET nombre_completo = %s, username = %s, password_hash = %s, id_tipo = %s, estado = %s WHERE id_usuario = %s"
        return self.ejecutar(sql, (dto.nombre_completo, dto.username, dto.password_hash, dto.id_tipo, dto.estado, dto.id_usuario))

    def eliminar(self, id_):
        return self.ejecutar("DELETE FROM usuario WHERE id_usuario = %s", (id_,))

    def obtener_por_username(self, username):
        filas = self.consultar("SELECT * FROM usuario WHERE username = %s", (username,))
        return UsuarioDTO(**filas[0]) if filas else None

    def existe_administrador(self):
        sql = ("SELECT COUNT(*) AS total FROM usuario u "
               "JOIN tipo_usuario t ON t.id_tipo = u.id_tipo "
               "WHERE t.nombre = 'Administrador'")
        return self.consultar(sql)[0]["total"] > 0
