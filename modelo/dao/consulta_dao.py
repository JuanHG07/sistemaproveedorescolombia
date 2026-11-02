from modelo.dao.base_dao import BaseDAO


class ConsultaDAO(BaseDAO):

    # ---------------- JOIN ----------------
    def proveedores_con_ubicacion(self) -> list:
        sql = ("SELECT d.nombre AS departamento, c.nombre AS ciudad, pr.nit, "
               "pr.razon_social, pr.telefono "
               "FROM proveedor pr "
               "JOIN ciudad c ON c.id_ciudad = pr.id_ciudad "
               "JOIN departamento d ON d.id_departamento = c.id_departamento "
               "ORDER BY d.nombre, c.nombre, pr.razon_social")
        return self._consultar(sql)

    def productos_con_categoria_y_proveedores(self) -> list:
        sql = ("SELECT p.codigo, p.nombre AS producto, ca.nombre AS categoria, "
               "pr.razon_social AS proveedor, pp.precio_unitario, pp.dias_entrega "
               "FROM producto p "
               "JOIN categoria ca ON ca.id_categoria = p.id_categoria "
               "JOIN proveedor_producto pp ON pp.id_producto = p.id_producto "
               "JOIN proveedor pr ON pr.id_proveedor = pp.id_proveedor "
               "ORDER BY p.nombre, pp.precio_unitario")
        return self._consultar(sql)

    def cobertura_por_ciudad(self) -> list:
        sql = ("SELECT d.nombre AS departamento, c.nombre AS ciudad, "
               "COUNT(DISTINCT pr.id_proveedor) AS proveedores, "
               "COUNT(pp.id_producto) AS productos_ofrecidos "
               "FROM departamento d "
               "JOIN ciudad c ON c.id_departamento = d.id_departamento "
               "JOIN proveedor pr ON pr.id_ciudad = c.id_ciudad "
               "LEFT JOIN proveedor_producto pp ON pp.id_proveedor = pr.id_proveedor "
               "GROUP BY d.id_departamento, d.nombre, c.id_ciudad, c.nombre "
               "ORDER BY d.nombre, c.nombre")
        return self._consultar(sql)

    # ---------------- Subconsultas ----------------
    def productos_con_precio_sobre_promedio(self) -> list:
        sql = ("SELECT p.codigo, p.nombre, p.unidad_medida "
               "FROM producto p "
               "WHERE p.id_producto IN ("
               "    SELECT pp.id_producto FROM proveedor_producto pp "
               "    WHERE pp.precio_unitario > ("
               "        SELECT AVG(precio_unitario) FROM proveedor_producto)) "
               "ORDER BY p.nombre")
        return self._consultar(sql)

    def proveedores_con_mas_de(self, minimo: int) -> list:
        sql = ("SELECT pr.nit, pr.razon_social, "
               "(SELECT COUNT(*) FROM proveedor_producto pp "
               " WHERE pp.id_proveedor = pr.id_proveedor) AS total_productos "
               "FROM proveedor pr "
               "WHERE (SELECT COUNT(*) FROM proveedor_producto pp "
               "       WHERE pp.id_proveedor = pr.id_proveedor) > %s "
               "ORDER BY total_productos DESC, pr.razon_social")
        return self._consultar(sql, (minimo,))