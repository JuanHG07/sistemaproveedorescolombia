from mysql.connector import Error
from controlador.base_controlador import BaseControlador
from controlador.sesion import Sesion
from modelo.dao.usuario_dao import UsuarioDAO
from modelo.dao.tipo_usuario_dao import TipoUsuarioDAO
from modelo.dao.bitacora_dao import BitacoraDAO
from utilidades import seguridad
from utilidades import validaciones as v
from utilidades.constantes import ACTIVO
from utilidades.errores import ErrorNegocio


class AuthControlador(BaseControlador):
    def __init__(self):
        self.usuarios = UsuarioDAO()
        self.tipos = TipoUsuarioDAO()
        self.bitacora = BitacoraDAO()

    def login(self, username, clave):
        def accion():
            if Sesion.usuario is not None:
                self.logout()
            nombre = v.texto(username, "usuario", 50)
            if not clave:
                raise ErrorNegocio("Ingrese la clave.")
            usuario = self.usuarios.obtener_por_username(nombre)
            if usuario is None or not seguridad.verificar(clave, usuario.password_hash):
                raise ErrorNegocio("Usuario o clave incorrectos.")
            if usuario.estado != ACTIVO:
                raise ErrorNegocio("La cuenta está inactiva. Contacte al administrador.")
            tipo = self.tipos.obtener_por_id(usuario.id_tipo)
            id_bitacora = self.bitacora.registrar_entrada(usuario.id_usuario)
            Sesion.iniciar(usuario, tipo.nombre, id_bitacora)
            return usuario
        return self._proteger(accion)

    def logout(self):
        if Sesion.id_bitacora is not None:
            try:
                self.bitacora.registrar_salida(Sesion.id_bitacora)
            except (Error, ConnectionError):
                pass
        Sesion.cerrar()
