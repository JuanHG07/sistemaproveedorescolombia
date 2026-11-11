from datetime import date, datetime
from decimal import Decimal

ESTADOS = (("A", "Activo"), ("I", "Inactivo"))


def texto(valor):
    if valor is None:
        return ""
    if isinstance(valor, (Decimal, float)):
        return f"{valor:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")
    if isinstance(valor, datetime):
        return valor.strftime("%d/%m/%Y %I:%M:%S %p")
    if isinstance(valor, date):
        return valor.strftime("%d/%m/%Y")
    return str(valor)


def estado(valor):
    return dict(ESTADOS).get(valor, valor)
