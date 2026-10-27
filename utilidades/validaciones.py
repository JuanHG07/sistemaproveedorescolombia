import re
from utilidades.constantes import ESTADOS


def no_vacio(valor, campo):
    if valor is None or str(valor).strip() == "":
        raise ValueError(f"El campo '{campo}' es obligatorio.")
    return str(valor).strip()


def correo_valido(correo):
    if correo and not re.match(r"^[\w.+-]+@[\w-]+\.[\w.-]+$", correo):
        raise ValueError("El correo no tiene un formato valido.")
    return correo


def numero_no_negativo(valor, campo):
    try:
        n = float(valor)
    except (TypeError, ValueError):
        raise ValueError(f"'{campo}' debe ser numerico.")
    if n < 0:
        raise ValueError(f"'{campo}' debe ser mayor o igual a 0.")
    return n


def estado_valido(estado):
    if estado not in ESTADOS:
        raise ValueError("El estado debe ser 'A' o 'I'.")
    return estado
