from modelo.dao.base_dao import BaseDAO


class ReporteDAO(BaseDAO):
    _ESTADO_TXT = "CASE {alias}.estado WHEN 'A' THEN 'Activo' ELSE 'Inactivo' END"

    def _con_filtros(self, select, filtros, cola):
        sql = select + " WHERE 1 = 1"
        params = []
        for fragmento, valor in filtros:
            if valor is not None:
                sql += f" AND {fragmento}"
                params.append(valor)
        return self._consultar(sql + " " + cola, tuple(params))

    def proveedores_por_ubicacion(self, id_departamento=None, id_ciudad=None, estado=None) -> list:
        select = ("SELECT d.nombre AS departamento, c.nombre AS ciudad, pr.nit, "
                  "pr.razon_social, pr.contacto, pr.telefono, "
                  + self._ESTADO_TXT.format(alias="pr") + " AS estado "
                  "FROM proveedor pr "
                  "JOIN ciudad c ON c.id_ciudad = pr.id_ciudad "
                  "JOIN departamento d ON d.id_departamento = c.id_departamento")
        return self._con_filtros(
            select,
            [("d.id_departamento = %s", id_departamento),
             ("c.id_ciudad = %s", id_ciudad),
             ("pr.estado = %s", estado)],
            "ORDER BY d.nombre, c.nombre, pr.razon_social")

    def proveedores_de_producto(self, id_producto=None) -> list:
        select = ("SELECT p.codigo, p.nombre AS producto, pr.razon_social AS proveedor, "
                  "c.nombre AS ciudad, pr.telefono, pp.precio_unitario, pp.dias_entrega "
                  "FROM proveedor_producto pp "
                  "JOIN producto p ON p.id_producto = pp.id_producto "
                  "JOIN proveedor pr ON pr.id_proveedor = pp.id_proveedor "
                  "JOIN ciudad c ON c.id_ciudad = pr.id_ciudad")
        return self._con_filtros(
            select, [("p.id_producto = %s", id_producto)],
            "ORDER BY p.nombre, pp.precio_unitario")

    def productos_de_proveedor(self, id_proveedor=None) -> list:
        select = ("SELECT pr.razon_social AS proveedor, p.codigo, p.nombre AS producto, "
                  "ca.nombre AS categoria, p.unidad_medida, pp.precio_unitario, pp.dias_entrega "
                  "FROM proveedor_producto pp "
                  "JOIN proveedor pr ON pr.id_proveedor = pp.id_proveedor "
                  "JOIN producto p ON p.id_producto = pp.id_producto "
                  "JOIN categoria ca ON ca.id_categoria = p.id_categoria")
        return self._con_filtros(
            select, [("pr.id_proveedor = %s", id_proveedor)],
            "ORDER BY pr.razon_social, p.nombre")

    def productos_por_categoria(self, id_categoria=None, estado=None) -> list:
        select = ("SELECT ca.nombre AS categoria, p.codigo, p.nombre AS producto, "
                  "p.unidad_medida, " + self._ESTADO_TXT.format(alias="p") + " AS estado "
                  "FROM producto p "
                  "JOIN categoria ca ON ca.id_categoria = p.id_categoria")
        return self._con_filtros(
            select,
            [("ca.id_categoria = %s", id_categoria),
             ("p.estado = %s", estado)],
            "ORDER BY ca.nombre, p.nombre")

    def resumen_por_categoria(self, id_categoria=None) -> list:
        select = ("SELECT ca.nombre AS categoria, "
                  "COUNT(DISTINCT p.id_producto) AS total_productos, "
                  "COUNT(DISTINCT pp.id_proveedor) AS proveedores, "
                  "ROUND(AVG(pp.precio_unitario), 2) AS precio_promedio "
                  "FROM categoria ca "
                  "LEFT JOIN producto p ON p.id_categoria = ca.id_categoria "
                  "LEFT JOIN proveedor_producto pp ON pp.id_producto = p.id_producto")
        return self._con_filtros(
            select, [("ca.id_categoria = %s", id_categoria)],
            "GROUP BY ca.id_categoria, ca.nombre ORDER BY ca.nombre")
