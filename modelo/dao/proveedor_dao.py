from modelo.dao.base_dao import BaseDAO
from modelo.dto.proveedor_dto import ProveedorDTO


class ProveedorDAO(BaseDAO):
    """Todo el SQL de la tabla proveedor."""

    def insertar(self, dto):
        sql = "INSERT INTO proveedor (nit, razon_social, contacto, telefono, correo, direccion, id_ciudad, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        return self.ejecutar(sql, (dto.nit, dto.razon_social, dto.contacto, dto.telefono, dto.correo, dto.direccion, dto.id_ciudad, dto.estado,))

    def listar(self):
        return [ProveedorDTO(**f) for f in self.consultar("SELECT * FROM proveedor")]

    def obtener(self, id_):
        filas = self.consultar("SELECT * FROM proveedor WHERE id_proveedor = %s", (id_,))
        return ProveedorDTO(**filas[0]) if filas else None

    def actualizar(self, dto):
        sql = "UPDATE proveedor SET nit = %s, razon_social = %s, contacto = %s, telefono = %s, correo = %s, direccion = %s, id_ciudad = %s, estado = %s WHERE id_proveedor = %s"
        return self.ejecutar(sql, (dto.nit, dto.razon_social, dto.contacto, dto.telefono, dto.correo, dto.direccion, dto.id_ciudad, dto.estado, dto.id_proveedor))

    def eliminar(self, id_):
        return self.ejecutar("DELETE FROM proveedor WHERE id_proveedor = %s", (id_,))
