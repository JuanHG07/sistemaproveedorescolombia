from modelo.dao.base_dao import BaseDAO
from modelo.dto.ciudad_dto import CiudadDTO


class CiudadDAO(BaseDAO):
    """Todo el SQL de la tabla ciudad."""

    def insertar(self, dto):
        sql = "INSERT INTO ciudad (nombre, id_departamento) VALUES (%s, %s)"
        return self.ejecutar(sql, (dto.nombre, dto.id_departamento,))

    def listar(self):
        return [CiudadDTO(**f) for f in self.consultar("SELECT * FROM ciudad")]

    def obtener(self, id_):
        filas = self.consultar("SELECT * FROM ciudad WHERE id_ciudad = %s", (id_,))
        return CiudadDTO(**filas[0]) if filas else None

    def actualizar(self, dto):
        sql = "UPDATE ciudad SET nombre = %s, id_departamento = %s WHERE id_ciudad = %s"
        return self.ejecutar(sql, (dto.nombre, dto.id_departamento, dto.id_ciudad))

    def eliminar(self, id_):
        return self.ejecutar("DELETE FROM ciudad WHERE id_ciudad = %s", (id_,))

    def listar_por_departamento(self, id_departamento):
        filas = self.consultar(
            "SELECT * FROM ciudad WHERE id_departamento = %s ORDER BY nombre",
            (id_departamento,))
        return [CiudadDTO(**f) for f in filas]
