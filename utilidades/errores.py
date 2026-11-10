from mysql.connector import Error


class ErrorNegocio(Exception):
    pass


def traducir_error(e: Error) -> str:
    codigo = getattr(e, "errno", None)
    texto = str(getattr(e, "msg", None) or e)

    if codigo == 1062:
        clave_msg = texto.split("for key")[-1]
        for clave, nombre in (("codigo", "código"), ("nit", "NIT"),
                              ("username", "nombre de usuario"), ("nombre", "nombre")):
            if clave in clave_msg:
                return f"Ya existe un registro con ese {nombre}."
        return "Ya existe un registro con esos datos."
    if codigo == 1451:
        return "No se puede eliminar: tiene registros relacionados."
    if codigo == 1452:
        return "El registro hace referencia a un dato que no existe."
    if codigo == 3819:
        return "Un valor no cumple las reglas de la base de datos."
    if codigo == 1406:
        return "Un texto es demasiado largo para el campo."
    if codigo == 1048:
        return "Falta un dato obligatorio."
    if codigo == 1264:
        return "Un valor numérico está fuera del rango permitido."
    return f"Error de base de datos: {texto}"
