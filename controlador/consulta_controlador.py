from controlador.base_controlador import BaseControlador
from modelo.dao.consulta_dao import ConsultaDAO
from utilidades import validaciones as v
from utilidades.errores import ErrorNegocio


class ConsultaControlador(BaseControlador):
    def __init__(self):
        self.dao = ConsultaDAO()
        self._consultas = {
            "join_ubicacion": ("JOIN: proveedores con ciudad y departamento",
                               self.dao.proveedores_con_ubicacion, None),
            "join_catalogo": ("JOIN: productos con categoría y proveedores",
                              self.dao.productos_con_categoria_y_proveedores, None),
            "join_cobertura": ("JOIN: cobertura de proveedores por ciudad",
                               self.dao.cobertura_por_ciudad, None),
            "sub_precio": ("Subconsulta: productos con algún proveedor sobre el precio promedio",
                           self.dao.productos_con_precio_sobre_promedio, None),
            "sub_proveedores": ("Subconsulta: proveedores con más de N productos",
                                self.dao.proveedores_con_mas_de, "mínimo de productos"),
        }

    def catalogo(self):
        return [(clave, t, p) for clave, (t, _, p) in self._consultas.items()]

    def ejecutar(self, clave, parametro=None):
        def accion():
            if clave not in self._consultas:
                raise ErrorNegocio("Consulta no reconocida.")
            titulo, funcion, etiqueta = self._consultas[clave]
            filas = funcion(v.entero_no_negativo(parametro, etiqueta)) if etiqueta else funcion()
            claves = list(filas[0].keys()) if filas else []   
            return {"titulo": titulo,
                    "encabezados": [k.replace("_", " ").capitalize() for k in claves],
                    "filas": filas}
        return self._leer(accion)