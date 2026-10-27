from controlador import permisos
from modelo.dao.bitacora_dao import BitacoraDAO


class BitacoraControlador:
    def __init__(self):
        self.dao = BitacoraDAO()

    def listar(self):
        permisos.exigir_admin()
        return self.dao.listar_detallado()
