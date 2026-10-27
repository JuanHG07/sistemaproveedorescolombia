from controlador.sesion import Sesion
from modelo.dao.usuario_dao import UsuarioDAO
from modelo.dao.tipo_usuario_dao import TipoUsuarioDAO
from modelo.dao.bitacora_dao import BitacoraDAO
from utilidades import seguridad
from utilidades.constantes import ACTIVO


class AuthControlador:
    def __init__(self):
        self.usuario_dao = UsuarioDAO()
        self.tipo_dao = TipoUsuarioDAO()
        self.bitacora_dao = BitacoraDAO()

    def login(self, username, clave):
        """Valida cuenta, clave y estado 'A'; registra la entrada en bitacora."""
        usuario = self.usuario_dao.obtener_por_username(username.strip())
        if usuario is None or not seguridad.verificar(clave, usuario.password_hash):
            raise ValueError("Usuario o clave incorrectos.")
        if usuario.estado != ACTIVO:
            raise ValueError("La cuenta esta inactiva.")
        tipo = self.tipo_dao.obtener(usuario.id_tipo).nombre
        id_bitacora = self.bitacora_dao.registrar_entrada(usuario.id_usuario)
        Sesion.iniciar(usuario, tipo, id_bitacora)
        return usuario

    def logout(self):
        """Actualiza fecha_hora_salida de la sesion activa."""
        if Sesion.id_bitacora:
            self.bitacora_dao.registrar_salida(Sesion.id_bitacora)
        Sesion.cerrar()
