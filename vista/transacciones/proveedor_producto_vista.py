import tkinter as tk
from tkinter import ttk


class ProveedorProductoVista(ttk.Frame):
    """Asignar productos a proveedores con precio_unitario y dias_entrega.

    Regla MVC: esta clase NO contiene SQL ni reglas de negocio;
    solo dibuja widgets y delega en el controlador.
    """

    def __init__(self, master=None):
        super().__init__(master)
        # TODO: construir interfaz
