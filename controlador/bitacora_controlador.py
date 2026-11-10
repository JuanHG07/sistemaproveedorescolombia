from controlador.base_controlador import BaseControlador
from modelo.dao.bitacora_dao import BitacoraDAO
from utilidades import validaciones as v


class BitacoraControlador(BaseControlador):

    def __init__(self):
        self.dao = BitacoraDAO()

    def listar(self):
        return self._como_admin(self.dao.listar_detallado)

    def listar_por_usuario(self, id_usuario):
        return self._como_admin(
            lambda: self.dao.listar_por_usuario(v.entero_positivo(id_usuario, "usuario")))
