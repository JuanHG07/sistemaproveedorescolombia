from modelo.dao.base_dao import BaseDAO
from modelo.dto.tipo_usuario_dto import TipoUsuarioDTO


class TipoUsuarioDAO(BaseDAO):
    """Todo el SQL de la tabla tipo_usuario."""

    def insertar(self, dto):
        sql = "INSERT INTO tipo_usuario (nombre) VALUES (%s)"
        return self.ejecutar(sql, (dto.nombre,))

    def listar(self):
        return [TipoUsuarioDTO(**f) for f in self.consultar("SELECT * FROM tipo_usuario")]

    def obtener(self, id_):
        filas = self.consultar("SELECT * FROM tipo_usuario WHERE id_tipo = %s", (id_,))
        return TipoUsuarioDTO(**filas[0]) if filas else None

    def actualizar(self, dto):
        sql = "UPDATE tipo_usuario SET nombre = %s WHERE id_tipo = %s"
        return self.ejecutar(sql, (dto.nombre, dto.id_tipo))

    def eliminar(self, id_):
        return self.ejecutar("DELETE FROM tipo_usuario WHERE id_tipo = %s", (id_,))
