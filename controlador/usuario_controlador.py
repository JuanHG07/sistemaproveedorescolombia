from controlador import permisos
from modelo.dao.usuario_dao import UsuarioDAO
from modelo.dao.tipo_usuario_dao import TipoUsuarioDAO
from modelo.dto.usuario_dto import UsuarioDTO
from utilidades import seguridad, validaciones
from utilidades.constantes import ADMIN


class UsuarioControlador:
    """Solo el Administrador gestiona cuentas."""

    def __init__(self):
        self.dao = UsuarioDAO()
        self.tipo_dao = TipoUsuarioDAO()

    def listar(self):
        permisos.exigir_admin()
        return self.dao.listar()

    def tipos(self):
        return self.tipo_dao.listar()

    def crear(self, nombre_completo, username, clave, id_tipo):
        permisos.exigir_admin()
        nombre_completo = validaciones.no_vacio(nombre_completo, "nombre completo")
        username = validaciones.no_vacio(username, "usuario")
        clave = validaciones.no_vacio(clave, "clave")
        if self.tipo_dao.obtener(id_tipo).nombre == ADMIN and self.dao.existe_administrador():
            raise ValueError("Ya existe un Administrador; solo puede haber uno.")
        dto = UsuarioDTO(None, nombre_completo, username, seguridad.hashear(clave), id_tipo, "A")
        return self.dao.insertar(dto)

    # TODO: actualizar / desactivar usuario (nunca el admin unico)
