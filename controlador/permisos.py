from controlador.sesion import Sesion
from utilidades.constantes import ADMIN, TRADICIONAL


def es_admin():
    return Sesion.tipo == ADMIN


def puede_escribir():
    """CRUD: Administrador y Tradicional."""
    return Sesion.tipo in (ADMIN, TRADICIONAL)


def puede_consultar():
    """Todos los perfiles autenticados."""
    return Sesion.tipo is not None


def exigir_escritura():
    if not puede_escribir():
        raise PermissionError("Su perfil solo permite consultas y reportes.")


def exigir_admin():
    if not es_admin():
        raise PermissionError("Solo el Administrador puede realizar esta accion.")
