from controlador import permisos
from modelo.dao.departamento_dao import DepartamentoDAO
from modelo.dto.departamento_dto import DepartamentoDTO


class DepartamentoControlador:
    def __init__(self):
        self.dao = DepartamentoDAO()

    def listar(self):
        return self.dao.listar()

    def guardar(self, dto: DepartamentoDTO):
        """Inserta (sin id) o actualiza (con id). TODO: validar campos con utilidades.validaciones."""
        permisos.exigir_escritura()
        pk = [v for v in vars(dto).values()][0]
        return self.dao.actualizar(dto) if pk else self.dao.insertar(dto)

    def eliminar(self, id_):
        """TODO: para producto/proveedor preferir borrado logico (estado='I')."""
        permisos.exigir_escritura()
        return self.dao.eliminar(id_)
