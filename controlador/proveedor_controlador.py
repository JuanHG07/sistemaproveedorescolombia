from controlador import permisos
from modelo.dao.proveedor_dao import ProveedorDAO
from modelo.dto.proveedor_dto import ProveedorDTO


class ProveedorControlador:
    def __init__(self):
        self.dao = ProveedorDAO()

    def listar(self):
        return self.dao.listar()

    def guardar(self, dto: ProveedorDTO):
        """Inserta (sin id) o actualiza (con id). TODO: validar campos con utilidades.validaciones."""
        permisos.exigir_escritura()
        pk = [v for v in vars(dto).values()][0]
        return self.dao.actualizar(dto) if pk else self.dao.insertar(dto)

    def eliminar(self, id_):
        """TODO: para producto/proveedor preferir borrado logico (estado='I')."""
        permisos.exigir_escritura()
        return self.dao.eliminar(id_)
