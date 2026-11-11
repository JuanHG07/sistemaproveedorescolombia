import tkinter as tk
from tkinter import ttk
from vista.componentes.formato import texto
from vista.componentes.tema import FILA_ALTERNA


class Tabla(ttk.Frame):
    def __init__(self, padre, columnas=(), al_doble_clic=None):
        super().__init__(padre, style="Tarjeta.TFrame", padding=1)
        self.arbol = ttk.Treeview(self, show="headings", selectmode="browse")
        vertical = ttk.Scrollbar(self, orient="vertical", command=self.arbol.yview)
        horizontal = ttk.Scrollbar(self, orient="horizontal", command=self.arbol.xview)
        self.arbol.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        self.arbol.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.arbol.tag_configure("par", background=FILA_ALTERNA)
        self._filas = []
        self._filtro = ""
        if al_doble_clic is not None:
            self.arbol.bind("<Double-1>", lambda e: al_doble_clic()
                            if self.arbol.identify_region(e.x, e.y) == "cell" else None)
        self.columnas(columnas)

    def columnas(self, columnas):
        claves = [clave for clave, _, _ in columnas]
        self.arbol.configure(columns=claves)
        for clave, titulo, ancho in columnas:
            self.arbol.heading(clave, text=titulo, anchor="w")
            self.arbol.column(clave, width=ancho, minwidth=60, anchor="w", stretch=True)

    def cargar(self, filas):
        self._filas = [(str(iid), tuple(texto(v) for v in valores)) for iid, valores in filas]
        return self.filtrar(self._filtro)

    def filtrar(self, filtro):
        self._filtro = filtro.strip().lower()
        self.arbol.delete(*self.arbol.get_children())
        visibles = [f for f in self._filas
                    if not self._filtro or any(self._filtro in v.lower() for v in f[1])]
        for i, (iid, valores) in enumerate(visibles):
            self.arbol.insert("", tk.END, iid=iid, values=valores,
                              tags=("par",) if i % 2 else ())
        return len(visibles)

    def seleccionado(self):
        seleccion = self.arbol.selection()
        return seleccion[0] if seleccion else None
