import tkinter as tk
from tkinter import ttk
from vista.componentes.selector import Selector
from vista.componentes.tema import (ACENTO, BLANCO, FONDO, FUENTE, PRIMARIO, TEXTO_CLARO,
                                    boton, centrar)


class Formulario(tk.Toplevel):
    def __init__(self, padre, titulo, al_guardar, subtitulo=""):
        super().__init__(padre)
        self.withdraw()
        self.title(titulo)
        self.configure(bg=FONDO)
        self.resizable(False, False)
        self.transient(padre.winfo_toplevel())
        self.guardado = False
        self._al_guardar = al_guardar
        self._campos = {}
        self._fila = 0

        encabezado = tk.Frame(self, bg=PRIMARIO, padx=24, pady=14)
        encabezado.pack(fill="x")
        tk.Label(encabezado, text=titulo, bg=PRIMARIO, fg=BLANCO,
                 font=(FUENTE, 14, "bold"), anchor="w").pack(fill="x")
        if subtitulo:
            tk.Label(encabezado, text=subtitulo, bg=PRIMARIO, fg=TEXTO_CLARO,
                     font=(FUENTE, 9), anchor="w").pack(fill="x")
        tk.Frame(self, bg=ACENTO, height=3).pack(fill="x")

        self.cuerpo = ttk.Frame(self, style="Plano.TFrame", padding=(24, 16, 24, 20))
        self.cuerpo.pack(fill="both", expand=True)
        self.cuerpo.columnconfigure(0, weight=1)

        pie = ttk.Frame(self, padding=(24, 12))
        pie.pack(fill="x")
        boton(pie, "Cancelar", "cancelar", self.destroy).pack(side="right")
        boton(pie, "Guardar", "guardar", self._guardar, "Primario").pack(side="right", padx=(0, 8))

        self.bind("<Return>", lambda _: self._guardar())
        self.bind("<Escape>", lambda _: self.destroy())

    def _etiqueta(self, texto):
        ttk.Label(self.cuerpo, text=texto, style="Campo.TLabel").grid(
            row=self._fila, column=0, sticky="w", pady=(10 if self._fila else 0, 3))
        self._fila += 1

    def _ubicar(self, widget):
        widget.grid(row=self._fila, column=0, sticky="ew")
        self._fila += 1

    def entrada(self, clave, etiqueta, valor=None, oculto=False):
        self._etiqueta(etiqueta)
        campo = ttk.Entry(self.cuerpo, width=44, show="•" if oculto else "")
        campo.insert(0, "" if valor is None else str(valor))
        self._ubicar(campo)
        self._campos[clave] = campo
        return campo

    def selector(self, clave, etiqueta, opciones, seleccionado=None, al_cambiar=None,
                 habilitado=True):
        self._etiqueta(etiqueta)
        campo = Selector(self.cuerpo, opciones, seleccionado, al_cambiar, ancho=42)
        campo.habilitar(habilitado)
        self._ubicar(campo)
        self._campos[clave] = campo
        return campo

    def nota(self, texto):
        ttk.Label(self.cuerpo, text=texto, style="Ayuda.TLabel", wraplength=380).grid(
            row=self._fila, column=0, sticky="w", pady=(8, 0))
        self._fila += 1

    def campo(self, clave):
        return self._campos[clave]

    def valor(self, clave):
        campo = self._campos[clave]
        return campo.valor() if isinstance(campo, Selector) else campo.get()

    def mostrar(self):
        self.update_idletasks()
        centrar(self, self.winfo_reqwidth(), self.winfo_reqheight(), self.master.winfo_toplevel())
        self.deiconify()
        self.grab_set()
        for campo in self._campos.values():
            if str(campo.cget("state")) not in ("disabled",):
                campo.focus_set()
                break
        self.wait_window()

    def _guardar(self):
        if self._al_guardar(self):
            self.guardado = True
            self.destroy()
