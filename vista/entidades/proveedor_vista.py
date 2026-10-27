import tkinter as tk
from tkinter import ttk


class ProveedorVista(ttk.Frame):
    """CRUD de proveedores (combos departamento -> ciudad).

    Regla MVC: esta clase NO contiene SQL ni reglas de negocio;
    solo dibuja widgets y delega en el controlador.
    """

    def __init__(self, master=None):
        super().__init__(master)
        # TODO: construir interfaz
