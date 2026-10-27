from modelo.dao.base_dao import BaseDAO
from modelo.dto.categoria_dto import CategoriaDTO


class CategoriaDAO(BaseDAO):
    """Todo el SQL de la tabla categoria."""

    def insertar(self, dto):
        sql = "INSERT INTO categoria (nombre, descripcion) VALUES (%s, %s)"
        return self.ejecutar(sql, (dto.nombre, dto.descripcion,))

    def listar(self):
        return [CategoriaDTO(**f) for f in self.consultar("SELECT * FROM categoria")]

    def obtener(self, id_):
        filas = self.consultar("SELECT * FROM categoria WHERE id_categoria = %s", (id_,))
        return CategoriaDTO(**filas[0]) if filas else None

    def actualizar(self, dto):
        sql = "UPDATE categoria SET nombre = %s, descripcion = %s WHERE id_categoria = %s"
        return self.ejecutar(sql, (dto.nombre, dto.descripcion, dto.id_categoria))

    def eliminar(self, id_):
        return self.ejecutar("DELETE FROM categoria WHERE id_categoria = %s", (id_,))
