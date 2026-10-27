from modelo.dao.base_dao import BaseDAO


class ReporteDAO(BaseDAO):
    """Datos filtrados para los 5 reportes. Filtros opcionales."""

    # --- Productos y proveedores (3) ---
    def proveedores_por_ubicacion(self, id_departamento=None, id_ciudad=None):
        sql = ("SELECT pr.nit, pr.razon_social, pr.telefono, c.nombre AS ciudad, d.nombre AS departamento "
               "FROM proveedor pr JOIN ciudad c ON c.id_ciudad = pr.id_ciudad "
               "JOIN departamento d ON d.id_departamento = c.id_departamento WHERE 1=1")
        p = []
        if id_departamento:
            sql += " AND d.id_departamento = %s"; p.append(id_departamento)
        if id_ciudad:
            sql += " AND c.id_ciudad = %s"; p.append(id_ciudad)
        return self.consultar(sql + " ORDER BY d.nombre, c.nombre", tuple(p))

    def proveedores_de_producto(self, id_producto):
        return self.consultar(
            "SELECT pr.razon_social, pr.telefono, pp.precio_unitario, pp.dias_entrega "
            "FROM proveedor_producto pp JOIN proveedor pr ON pr.id_proveedor = pp.id_proveedor "
            "WHERE pp.id_producto = %s ORDER BY pp.precio_unitario", (id_producto,))

    def productos_de_proveedor(self, id_proveedor):
        return self.consultar(
            "SELECT p.codigo, p.nombre, p.unidad_medida, pp.precio_unitario, pp.dias_entrega "
            "FROM proveedor_producto pp JOIN producto p ON p.id_producto = pp.id_producto "
            "WHERE pp.id_proveedor = %s ORDER BY p.nombre", (id_proveedor,))

    # --- Productos y categorias (2) ---
    def productos_por_categoria(self, id_categoria=None, estado=None):
        sql = ("SELECT ca.nombre AS categoria, p.codigo, p.nombre, p.unidad_medida, p.estado "
               "FROM producto p JOIN categoria ca ON ca.id_categoria = p.id_categoria WHERE 1=1")
        p = []
        if id_categoria:
            sql += " AND ca.id_categoria = %s"; p.append(id_categoria)
        if estado:
            sql += " AND p.estado = %s"; p.append(estado)
        return self.consultar(sql + " ORDER BY ca.nombre, p.nombre", tuple(p))

    def resumen_por_categoria(self, id_categoria=None):
        sql = ("SELECT ca.nombre AS categoria, COUNT(DISTINCT p.id_producto) AS total_productos, "
               "ROUND(AVG(pp.precio_unitario), 2) AS precio_promedio "
               "FROM categoria ca LEFT JOIN producto p ON p.id_categoria = ca.id_categoria "
               "LEFT JOIN proveedor_producto pp ON pp.id_producto = p.id_producto")
        p = []
        if id_categoria:
            sql += " WHERE ca.id_categoria = %s"; p.append(id_categoria)
        return self.consultar(sql + " GROUP BY ca.id_categoria, ca.nombre ORDER BY ca.nombre", tuple(p))
