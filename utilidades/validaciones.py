import math
import re
from utilidades.constantes import ESTADOS
from utilidades.errores import ErrorNegocio


def texto(valor, campo, maximo, obligatorio=True):
    t = "" if valor is None else str(valor).strip()
    if not t:
        if obligatorio:
            raise ErrorNegocio(f"El campo '{campo}' es obligatorio.")
        return None
    if len(t) > maximo:
        raise ErrorNegocio(f"'{campo}' no puede superar {maximo} caracteres.")
    return t


def entero_positivo(valor, campo):
    try:
        n = int(valor)
    except (TypeError, ValueError):
        raise ErrorNegocio(f"Seleccione un valor válido para '{campo}'.")
    if n <= 0:
        raise ErrorNegocio(f"Seleccione un valor válido para '{campo}'.")
    return n


def entero_opcional(valor):
    try:
        n = int(valor)
    except (TypeError, ValueError):
        return None
    return n if n > 0 else None


def numero_no_negativo(valor, campo):
    try:
        n = float(str(valor).strip().replace(",", "."))
    except ValueError:
        raise ErrorNegocio(f"'{campo}' debe ser un número.")
    if not math.isfinite(n) or n < 0:
        raise ErrorNegocio(f"'{campo}' debe ser un número mayor o igual a 0.")
    return n


def entero_no_negativo(valor, campo):
    n = numero_no_negativo(valor, campo)
    if n != int(n):
        raise ErrorNegocio(f"'{campo}' debe ser un número entero.")
    return int(n)


def correo(valor):
    c = texto(valor, "correo", 100, obligatorio=False)
    if c and not re.match(r"^[\w.+-]+@[\w-]+\.[\w.-]+$", c):
        raise ErrorNegocio("El correo no tiene un formato válido.")
    return c


def telefono(valor):
    t = texto(valor, "teléfono", 20)
    if not re.match(r"^[0-9+\-\s()]{7,20}$", t):
        raise ErrorNegocio("El teléfono solo puede tener números, espacios, +, - y paréntesis (mínimo 7).")
    return t


def nit(valor):
    n = texto(valor, "NIT", 20)
    if not re.match(r"^\d[\d.\-]*$", n):
        raise ErrorNegocio("El NIT solo puede tener números, puntos y guion.")
    return n


def estado(valor):
    if valor not in ESTADOS:
        raise ErrorNegocio("El estado debe ser 'A' (activo) o 'I' (inactivo).")
    return valor


def clave(valor):
    if valor is None or len(valor) < 6:
        raise ErrorNegocio("La clave debe tener al menos 6 caracteres.")
    return valor
