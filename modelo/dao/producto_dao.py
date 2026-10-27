from modelo.dao.base_dao import BaseDAO
from modelo.dto.producto_dto import ProductoDTO


class ProductoDAO(BaseDAO):
    """Todo el SQL de la tabla producto."""

    def insertar(self, dto):
        sql = "INSERT INTO producto (codigo, nombre, descripcion, unidad_medida, id_categoria, estado) VALUES (%s, %s, %s, %s, %s, %s)"
        return self.ejecutar(sql, (dto.codigo, dto.nombre, dto.descripcion, dto.unidad_medida, dto.id_categoria, dto.estado,))

    def listar(self):
        return [ProductoDTO(**f) for f in self.consultar("SELECT * FROM producto")]

    def obtener(self, id_):
        filas = self.consultar("SELECT * FROM producto WHERE id_producto = %s", (id_,))
        return ProductoDTO(**filas[0]) if filas else None

    def actualizar(self, dto):
        sql = "UPDATE producto SET codigo = %s, nombre = %s, descripcion = %s, unidad_medida = %s, id_categoria = %s, estado = %s WHERE id_producto = %s"
        return self.ejecutar(sql, (dto.codigo, dto.nombre, dto.descripcion, dto.unidad_medida, dto.id_categoria, dto.estado, dto.id_producto))

    def eliminar(self, id_):
        return self.ejecutar("DELETE FROM producto WHERE id_producto = %s", (id_,))
