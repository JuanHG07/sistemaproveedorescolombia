import tkinter as tk
from tkinter import ttk


class CategoriaVista(ttk.Frame):
    """CRUD de categorias.

    Regla MVC: esta clase NO contiene SQL ni reglas de negocio;
    solo dibuja widgets y delega en el controlador.
    """

    def __init__(self, master=None):
        super().__init__(master)
        # TODO: construir interfaz
