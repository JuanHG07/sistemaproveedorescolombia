from controlador import permisos
from controlador.base_controlador import BaseControlador
from controlador.sesion import Sesion
from modelo.dao.usuario_dao import UsuarioDAO
from modelo.dao.tipo_usuario_dao import TipoUsuarioDAO
from modelo.dto.usuario import Usuario
from utilidades import seguridad
from utilidades import validaciones as v
from utilidades.constantes import ADMIN, ACTIVO
from utilidades.errores import ErrorNegocio


class UsuarioControlador(BaseControlador):

    def __init__(self):
        self.dao = UsuarioDAO()
        self.tipos = TipoUsuarioDAO()

    def listar(self):
        return self._como_admin(self.dao.listar)

    def listar_tipos(self):
        return self._como_admin(self.tipos.listar)

    def crear(self, nombre_completo, username, clave, id_tipo):
        def accion():
            tipo = self._tipo_valido(id_tipo)
            if tipo.nombre == ADMIN:
                self._validar_unico_admin()
            usuario = Usuario(
                nombre_completo=v.texto(nombre_completo, "nombre completo", 120),
                username=v.texto(username, "usuario", 50),
                password_hash=seguridad.hashear(v.clave(clave)),
                id_tipo=tipo.id_tipo,
                estado=ACTIVO)
            return self.dao.insertar(usuario)
        return self._como_admin(accion)

    def actualizar(self, id_usuario, nombre_completo, username, id_tipo, estado):
        def accion():
            actual = self.dao.obtener_por_id(id_usuario)
            self._debe_existir(actual, "El usuario")
            tipo_actual = self.tipos.obtener_por_id(actual.id_tipo)
            tipo_nuevo = self._tipo_valido(id_tipo)
            estado_nuevo = v.estado(estado)
            if tipo_actual.nombre == ADMIN:
                if tipo_nuevo.nombre != ADMIN:
                    raise ErrorNegocio("No se puede cambiar el tipo del Administrador.")
                if estado_nuevo != ACTIVO:
                    raise ErrorNegocio("No se puede desactivar al Administrador.")
            elif tipo_nuevo.nombre == ADMIN:
                self._validar_unico_admin()
            self.dao.actualizar(Usuario(
                id_usuario=id_usuario,
                nombre_completo=v.texto(nombre_completo, "nombre completo", 120),
                username=v.texto(username, "usuario", 50),
                password_hash=actual.password_hash,
                id_tipo=tipo_nuevo.id_tipo,
                estado=estado_nuevo))
        self._como_admin(accion)

    def cambiar_estado(self, id_usuario, estado):
        def accion():
            usuario = self.dao.obtener_por_id(id_usuario)
            self._debe_existir(usuario, "El usuario")
            nuevo = v.estado(estado)
            if nuevo != ACTIVO and self.tipos.obtener_por_id(usuario.id_tipo).nombre == ADMIN:
                raise ErrorNegocio("No se puede desactivar al Administrador.")
            self.dao.cambiar_estado(id_usuario, nuevo)
        self._como_admin(accion)

    def restablecer_password(self, id_usuario, clave_nueva):
        def accion():
            self._debe_existir(self.dao.obtener_por_id(id_usuario), "El usuario")
            self.dao.actualizar_password(id_usuario, seguridad.hashear(v.clave(clave_nueva)))
        self._como_admin(accion)

    def cambiar_mi_password(self, clave_actual, clave_nueva):
        permisos.exigir_sesion()
        def accion():
            usuario = self.dao.obtener_por_id(Sesion.usuario.id_usuario)
            if not seguridad.verificar(clave_actual or "", usuario.password_hash):
                raise ErrorNegocio("La clave actual es incorrecta.")
            self.dao.actualizar_password(usuario.id_usuario, seguridad.hashear(v.clave(clave_nueva)))
        self._proteger(accion)

    def _tipo_valido(self, id_tipo):
        tipo = self.tipos.obtener_por_id(v.entero_positivo(id_tipo, "tipo de usuario"))
        if tipo is None:
            raise ErrorNegocio("El tipo de usuario no existe.")
        return tipo

    def _validar_unico_admin(self):
        if self.dao.contar_por_tipo(ADMIN) > 0:
            raise ErrorNegocio("Ya existe un Administrador; solo puede haber uno.")
