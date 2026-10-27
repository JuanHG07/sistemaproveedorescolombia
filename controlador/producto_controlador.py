from controlador import permisos
from modelo.dao.producto_dao import ProductoDAO
from modelo.dto.producto_dto import ProductoDTO


class ProductoControlador:
    def __init__(self):
        self.dao = ProductoDAO()

    def listar(self):
        return self.dao.listar()

    def guardar(self, dto: ProductoDTO):
        """Inserta (sin id) o actualiza (con id). TODO: validar campos con utilidades.validaciones."""
        permisos.exigir_escritura()
        pk = [v for v in vars(dto).values()][0]
        return self.dao.actualizar(dto) if pk else self.dao.insertar(dto)

    def eliminar(self, id_):
        """TODO: para producto/proveedor preferir borrado logico (estado='I')."""
        permisos.exigir_escritura()
        return self.dao.eliminar(id_)
