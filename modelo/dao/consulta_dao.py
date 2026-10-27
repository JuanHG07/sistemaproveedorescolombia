from modelo.dao.base_dao import BaseDAO


class ConsultaDAO(BaseDAO):
    """3 consultas con JOIN (3+ tablas) y 2 con subconsultas."""

    def join_proveedores_ubicacion(self):
        # JOIN 1: proveedor + ciudad + departamento
        return self.consultar(
            "SELECT pr.nit, pr.razon_social, c.nombre AS ciudad, d.nombre AS departamento "
            "FROM proveedor pr "
            "JOIN ciudad c ON c.id_ciudad = pr.id_ciudad "
            "JOIN departamento d ON d.id_departamento = c.id_departamento "
            "ORDER BY d.nombre, c.nombre")

    def join_productos_proveedores(self):
        # JOIN 2: producto + categoria + proveedor_producto + proveedor
        return self.consultar(
            "SELECT p.codigo, p.nombre AS producto, ca.nombre AS categoria, "
            "pr.razon_social AS proveedor, pp.precio_unitario, pp.dias_entrega "
            "FROM producto p "
            "JOIN categoria ca ON ca.id_categoria = p.id_categoria "
            "JOIN proveedor_producto pp ON pp.id_producto = p.id_producto "
            "JOIN proveedor pr ON pr.id_proveedor = pp.id_proveedor "
            "ORDER BY p.nombre")

    def join_accesos_usuarios(self):
        # JOIN 3: usuario + tipo_usuario + bitacora
        return self.consultar(
            "SELECT u.username, t.nombre AS tipo, b.fecha_hora_entrada, b.fecha_hora_salida "
            "FROM usuario u "
            "JOIN tipo_usuario t ON t.id_tipo = u.id_tipo "
            "JOIN bitacora b ON b.id_usuario = u.id_usuario "
            "ORDER BY b.fecha_hora_entrada DESC")

    def sub_precio_sobre_promedio(self):
        # Subconsulta 1: producto + proveedor_producto
        return self.consultar(
            "SELECT p.codigo, p.nombre, pp.precio_unitario "
            "FROM producto p JOIN proveedor_producto pp ON pp.id_producto = p.id_producto "
            "WHERE pp.precio_unitario > (SELECT AVG(precio_unitario) FROM proveedor_producto) "
            "ORDER BY pp.precio_unitario DESC")

    def sub_proveedores_con_mas_de(self, n):
        # Subconsulta 2: proveedor + proveedor_producto
        return self.consultar(
            "SELECT pr.nit, pr.razon_social FROM proveedor pr "
            "WHERE (SELECT COUNT(*) FROM proveedor_producto pp "
            "       WHERE pp.id_proveedor = pr.id_proveedor) > %s", (n,))
