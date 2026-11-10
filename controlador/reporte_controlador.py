from controlador.base_controlador import BaseControlador
from modelo.dao.reporte_dao import ReporteDAO
from modelo.dao.departamento_dao import DepartamentoDAO
from modelo.dao.ciudad_dao import CiudadDAO
from modelo.dao.producto_dao import ProductoDAO
from modelo.dao.proveedor_dao import ProveedorDAO
from modelo.dao.categoria_dao import CategoriaDAO
from utilidades import validaciones as v

_ESTADOS_TXT = {"A": "Activo", "I": "Inactivo"}


class ReporteControlador(BaseControlador):

    def __init__(self):
        self.dao = ReporteDAO()
        self._departamentos = DepartamentoDAO()
        self._ciudades = CiudadDAO()
        self._productos = ProductoDAO()
        self._proveedores = ProveedorDAO()
        self._categorias = CategoriaDAO()

    def proveedores_por_ubicacion(self, id_departamento=None, id_ciudad=None, estado=None):
        def accion():
            idd = v.entero_opcional(id_departamento)
            idc = v.entero_opcional(id_ciudad)
            est = self._estado_opcional(estado)
            filas = self.dao.proveedores_por_ubicacion(idd, idc, est)
            return self._armar(
                "Proveedores por ubicación",
                [("departamento", "Departamento"), ("ciudad", "Ciudad"), ("nit", "NIT"),
                 ("razon_social", "Razón social"), ("contacto", "Contacto"),
                 ("telefono", "Teléfono"), ("estado", "Estado")],
                filas,
                [self._filtro("Departamento", idd, self._departamentos.obtener_por_id, "nombre"),
                 self._filtro("Ciudad", idc, self._ciudades.obtener_por_id, "nombre"),
                 f"Estado: {_ESTADOS_TXT[est]}" if est else None])
        return self._leer(accion)

    def proveedores_de_producto(self, id_producto=None):
        def accion():
            idp = v.entero_opcional(id_producto)
            filas = self.dao.proveedores_de_producto(idp)
            return self._armar(
                "Proveedores por producto",
                [("codigo", "Código"), ("producto", "Producto"), ("proveedor", "Proveedor"),
                 ("ciudad", "Ciudad"), ("telefono", "Teléfono"),
                 ("precio_unitario", "Precio unitario"), ("dias_entrega", "Días de entrega")],
                filas,
                [self._filtro("Producto", idp, self._productos.obtener_por_id, "nombre")])
        return self._leer(accion)

    def productos_de_proveedor(self, id_proveedor=None):
        def accion():
            idp = v.entero_opcional(id_proveedor)
            filas = self.dao.productos_de_proveedor(idp)
            return self._armar(
                "Productos por proveedor",
                [("proveedor", "Proveedor"), ("codigo", "Código"), ("producto", "Producto"),
                 ("categoria", "Categoría"), ("unidad_medida", "Unidad"),
                 ("precio_unitario", "Precio unitario"), ("dias_entrega", "Días de entrega")],
                filas,
                [self._filtro("Proveedor", idp, self._proveedores.obtener_por_id, "razon_social")])
        return self._leer(accion)

    def productos_por_categoria(self, id_categoria=None, estado=None):
        def accion():
            idc = v.entero_opcional(id_categoria)
            est = self._estado_opcional(estado)
            filas = self.dao.productos_por_categoria(idc, est)
            return self._armar(
                "Productos por categoría",
                [("categoria", "Categoría"), ("codigo", "Código"), ("producto", "Producto"),
                 ("unidad_medida", "Unidad"), ("estado", "Estado")],
                filas,
                [self._filtro("Categoría", idc, self._categorias.obtener_por_id, "nombre"),
                 f"Estado: {_ESTADOS_TXT[est]}" if est else None])
        return self._leer(accion)

    def resumen_por_categoria(self, id_categoria=None):
        def accion():
            idc = v.entero_opcional(id_categoria)
            filas = self.dao.resumen_por_categoria(idc)
            return self._armar(
                "Resumen por categoría",
                [("categoria", "Categoría"), ("total_productos", "Total de productos"),
                 ("proveedores", "Proveedores"), ("precio_promedio", "Precio promedio")],
                filas,
                [self._filtro("Categoría", idc, self._categorias.obtener_por_id, "nombre")])
        return self._leer(accion)

    @staticmethod
    def _estado_opcional(estado):
        return None if estado in (None, "", "Todos") else v.estado(estado)

    @staticmethod
    def _filtro(etiqueta, id_, obtener, atributo):
        if id_ is None:
            return None
        objeto = obtener(id_)
        return f"{etiqueta}: {getattr(objeto, atributo)}" if objeto else None

    @staticmethod
    def _armar(titulo, columnas, filas, filtros):
        return {
            "titulo": titulo,
            "encabezados": [encabezado for _, encabezado in columnas],
            "filas": [tuple("" if f[clave] is None else f[clave] for clave, _ in columnas)
                      for f in filas],
            "filtros": ", ".join(x for x in filtros if x) or "Sin filtros",
        }
