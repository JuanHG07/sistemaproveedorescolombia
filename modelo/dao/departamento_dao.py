from modelo.dao.base_dao import BaseDAO
from modelo.dto.departamento_dto import DepartamentoDTO


class DepartamentoDAO(BaseDAO):
    """Todo el SQL de la tabla departamento."""

    def insertar(self, dto):
        sql = "INSERT INTO departamento (nombre) VALUES (%s)"
        return self.ejecutar(sql, (dto.nombre,))

    def listar(self):
        return [DepartamentoDTO(**f) for f in self.consultar("SELECT * FROM departamento")]

    def obtener(self, id_):
        filas = self.consultar("SELECT * FROM departamento WHERE id_departamento = %s", (id_,))
        return DepartamentoDTO(**filas[0]) if filas else None

    def actualizar(self, dto):
        sql = "UPDATE departamento SET nombre = %s WHERE id_departamento = %s"
        return self.ejecutar(sql, (dto.nombre, dto.id_departamento))

    def eliminar(self, id_):
        return self.ejecutar("DELETE FROM departamento WHERE id_departamento = %s", (id_,))
