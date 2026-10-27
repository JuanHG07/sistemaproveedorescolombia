from modelo.dao.base_dao import BaseDAO
from modelo.dto.bitacora_dto import BitacoraDTO


class BitacoraDAO(BaseDAO):
    """Todo el SQL de la tabla bitacora."""

    def insertar(self, dto):
        sql = "INSERT INTO bitacora (id_usuario, fecha_hora_entrada, fecha_hora_salida) VALUES (%s, %s, %s)"
        return self.ejecutar(sql, (dto.id_usuario, dto.fecha_hora_entrada, dto.fecha_hora_salida,))

    def listar(self):
        return [BitacoraDTO(**f) for f in self.consultar("SELECT * FROM bitacora")]

    def obtener(self, id_):
        filas = self.consultar("SELECT * FROM bitacora WHERE id_bitacora = %s", (id_,))
        return BitacoraDTO(**filas[0]) if filas else None

    def actualizar(self, dto):
        sql = "UPDATE bitacora SET id_usuario = %s, fecha_hora_entrada = %s, fecha_hora_salida = %s WHERE id_bitacora = %s"
        return self.ejecutar(sql, (dto.id_usuario, dto.fecha_hora_entrada, dto.fecha_hora_salida, dto.id_bitacora))

    def eliminar(self, id_):
        return self.ejecutar("DELETE FROM bitacora WHERE id_bitacora = %s", (id_,))

    def registrar_entrada(self, id_usuario):
        """Inserta la sesion y devuelve id_bitacora."""
        return self.ejecutar(
            "INSERT INTO bitacora (id_usuario, fecha_hora_entrada) VALUES (%s, NOW())",
            (id_usuario,))

    def registrar_salida(self, id_bitacora):
        return self.ejecutar(
            "UPDATE bitacora SET fecha_hora_salida = NOW() WHERE id_bitacora = %s",
            (id_bitacora,))

    def listar_detallado(self):
        sql = ("SELECT b.id_bitacora, u.username, u.nombre_completo, t.nombre AS tipo, "
               "b.fecha_hora_entrada, b.fecha_hora_salida "
               "FROM bitacora b JOIN usuario u ON u.id_usuario = b.id_usuario "
               "JOIN tipo_usuario t ON t.id_tipo = u.id_tipo "
               "ORDER BY b.fecha_hora_entrada DESC")
        return self.consultar(sql)
