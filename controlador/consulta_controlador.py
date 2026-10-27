from modelo.dao.consulta_dao import ConsultaDAO


class ConsultaControlador:
    def __init__(self):
        self.dao = ConsultaDAO()

    def catalogo(self):
        """Nombre visible -> funcion que devuelve las filas."""
        return {
            "JOIN: Proveedores por ciudad y departamento": self.dao.join_proveedores_ubicacion,
            "JOIN: Productos, categorias y proveedores": self.dao.join_productos_proveedores,
            "JOIN: Accesos de usuarios (bitacora)": self.dao.join_accesos_usuarios,
            "Subconsulta: Precios sobre el promedio": self.dao.sub_precio_sobre_promedio,
            "Subconsulta: Proveedores con mas de 2 productos": lambda: self.dao.sub_proveedores_con_mas_de(2),
        }
