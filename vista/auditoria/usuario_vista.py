from controlador.usuario_controlador import UsuarioControlador
from utilidades.errores import ErrorNegocio
from vista.componentes.dialogos import ejecutar, informar
from vista.componentes.formato import ESTADOS, estado
from vista.componentes.formulario import Formulario
from vista.componentes.tema import boton
from vista.componentes.vista_crud import VistaCrud


def claves_iguales(formulario, clave="clave", confirmacion="confirmacion"):
    if formulario.valor(clave) != formulario.valor(confirmacion):
        raise ErrorNegocio("La clave y su confirmación no coinciden.")
    return formulario.valor(clave)


class UsuarioVista(VistaCrud):
    titulo = "Gestión de usuarios"
    descripcion = "Cuentas con acceso al sistema. Solo el Administrador puede crearlas o modificarlas."
    singular = "usuario"
    permite_eliminar = False
    columnas = (("nombre", "Nombre completo", 280), ("usuario", "Usuario", 160),
                ("tipo", "Perfil", 160), ("estado", "Estado", 100))

    def __init__(self, padre):
        self.controlador = UsuarioControlador()
        self.tipos = {}
        super().__init__(padre)

    def acciones_extra(self, barra):
        boton(barra, "Restablecer clave", "clave", self._restablecer).pack(side="left", padx=(8, 0))

    def obtener_registros(self):
        self.tipos = {t.id_tipo: t.nombre for t in self.controlador.listar_tipos()}
        return self.controlador.listar()

    def clave(self, registro):
        return registro.id_usuario

    def fila(self, registro):
        return (registro.nombre_completo, registro.username,
                self.tipos.get(registro.id_tipo), estado(registro.estado))

    def campos(self, formulario, registro):
        formulario.entrada("nombre", "Nombre completo", registro and registro.nombre_completo)
        formulario.entrada("usuario", "Nombre de usuario", registro and registro.username)
        if registro is None:
            formulario.entrada("clave", "Clave", oculto=True)
            formulario.entrada("confirmacion", "Confirmar clave", oculto=True)
        formulario.selector("tipo", "Perfil", self.tipos.items(), registro and registro.id_tipo)
        if registro is not None:
            formulario.selector("estado", "Estado", ESTADOS, registro.estado)
        formulario.nota("Tradicional: gestiona datos. Esporádico: solo consultas y reportes.")

    def guardar(self, formulario, registro):
        if registro is None:
            self.controlador.crear(formulario.valor("nombre"), formulario.valor("usuario"),
                                   claves_iguales(formulario), formulario.valor("tipo"))
        else:
            self.controlador.actualizar(registro.id_usuario, formulario.valor("nombre"),
                                        formulario.valor("usuario"), formulario.valor("tipo"),
                                        formulario.valor("estado"))

    def _restablecer(self):
        registro = self.seleccionado()
        if registro is None:
            return
        formulario = Formulario(self, "Restablecer clave", lambda f: ejecutar(
            f, lambda: self.controlador.restablecer_password(registro.id_usuario,
                                                             claves_iguales(f)))[0],
            f"Usuario: {registro.username}")
        formulario.entrada("clave", "Nueva clave", oculto=True)
        formulario.entrada("confirmacion", "Confirmar clave", oculto=True)
        formulario.mostrar()
        if formulario.guardado:
            informar(self, "La clave se restableció correctamente.")
