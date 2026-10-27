from modelo.dao.reporte_dao import ReporteDAO
from utilidades.generador_pdf import generar_pdf


class ReporteControlador:
    """Obtiene datos filtrados y genera el PDF. TODO: enlazar con reportes_vista."""

    def __init__(self):
        self.dao = ReporteDAO()

    def proveedores_por_ubicacion(self, id_departamento=None, id_ciudad=None):
        filas = self.dao.proveedores_por_ubicacion(id_departamento, id_ciudad)
        enc = ["NIT", "Razon social", "Telefono", "Ciudad", "Departamento"]
        datos = [(f["nit"], f["razon_social"], f["telefono"], f["ciudad"], f["departamento"]) for f in filas]
        return generar_pdf("Proveedores por ubicacion", enc, datos, "proveedores_ubicacion")

    # TODO: proveedores_de_producto, productos_de_proveedor,
    #       productos_por_categoria, resumen_por_categoria
