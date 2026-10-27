from controlador import permisos
from modelo.dao.categoria_dao import CategoriaDAO
from modelo.dto.categoria_dto import CategoriaDTO


class CategoriaControlador:
    def __init__(self):
        self.dao = CategoriaDAO()

    def listar(self):
        return self.dao.listar()

    def guardar(self, dto: CategoriaDTO):
        """Inserta (sin id) o actualiza (con id). TODO: validar campos con utilidades.validaciones."""
        permisos.exigir_escritura()
        pk = [v for v in vars(dto).values()][0]
        return self.dao.actualizar(dto) if pk else self.dao.insertar(dto)

    def eliminar(self, id_):
        """TODO: para producto/proveedor preferir borrado logico (estado='I')."""
        permisos.exigir_escritura()
        return self.dao.eliminar(id_)
