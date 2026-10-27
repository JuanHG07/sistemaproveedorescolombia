import tkinter as tk
from tkinter import ttk


class TablaBase(ttk.Frame):
    """Treeview reutilizable con scroll y ordenamiento.

    Regla MVC: esta clase NO contiene SQL ni reglas de negocio;
    solo dibuja widgets y delega en el controlador.
    """

    def __init__(self, master=None):
        super().__init__(master)
        # TODO: construir interfaz
