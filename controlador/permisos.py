from controlador.sesion import Sesion
from utilidades.constantes import ADMIN, TRADICIONAL
from utilidades.errores import ErrorNegocio


def hay_sesion():
    return Sesion.usuario is not None


def es_admin():
    return Sesion.tipo == ADMIN


def puede_escribir():
    return Sesion.tipo in (ADMIN, TRADICIONAL)


def exigir_sesion():
    if not hay_sesion():
        raise ErrorNegocio("Debe iniciar sesión para continuar.")


def exigir_escritura():
    exigir_sesion()
    if not puede_escribir():
        raise ErrorNegocio("Su perfil solo permite consultas y reportes.")


def exigir_admin():
    exigir_sesion()
    if not es_admin():
        raise ErrorNegocio("Solo el Administrador puede realizar esta acción.")
