from tkinter import messagebox
from utilidades.errores import ErrorNegocio
from vista.componentes.tema import TITULO_APP


def ejecutar(padre, accion):
    try:
        return True, accion()
    except ErrorNegocio as e:
        messagebox.showerror(TITULO_APP, str(e), parent=padre)
        return False, None


def confirmar(padre, mensaje):
    return messagebox.askyesno(TITULO_APP, mensaje, parent=padre, icon="warning")


def informar(padre, mensaje):
    messagebox.showinfo(TITULO_APP, mensaje, parent=padre)
