from tkinter import ttk


class Selector(ttk.Combobox):
    def __init__(self, padre, opciones=(), seleccionado=None, al_cambiar=None, ancho=40):
        super().__init__(padre, state="readonly", width=ancho)
        self._opciones = []
        self.opciones(opciones, seleccionado)
        if al_cambiar is not None:
            self.bind("<<ComboboxSelected>>", lambda _: al_cambiar(self.valor()))

    def opciones(self, opciones, seleccionado=None):
        self._opciones = list(opciones)
        self["values"] = [texto for _, texto in self._opciones]
        self.seleccionar(seleccionado)

    def seleccionar(self, valor):
        for i, (clave, _) in enumerate(self._opciones):
            if clave == valor:
                self.current(i)
                return
        if self._opciones and self._opciones[0][0] is None:
            self.current(0)
        else:
            self.set("")

    def valor(self):
        i = self.current()
        return self._opciones[i][0] if i >= 0 else None

    def habilitar(self, activo):
        self.configure(state="readonly" if activo else "disabled")
