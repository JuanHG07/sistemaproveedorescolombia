from tkinter import ttk
from controlador.consulta_controlador import ConsultaControlador
from vista.componentes.dialogos import ejecutar
from vista.componentes.selector import Selector
from vista.componentes.tabla import Tabla
from vista.componentes.tema import boton


class ConsultaVista(ttk.Frame):
    def __init__(self, padre, clave=None):
        super().__init__(padre, padding=(28, 22))
        self.controlador = ConsultaControlador()
        self._catalogo = {c: (titulo, etiqueta) for c, titulo, etiqueta in self.controlador.catalogo()}

        ttk.Label(self, text="Consultas", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(self, text="Consultas que cruzan la información de varias tablas de la base de datos.",
                  style="Descripcion.TLabel").pack(anchor="w", pady=(2, 14))

        panel = ttk.Frame(self, style="Tarjeta.TFrame", padding=(18, 14))
        panel.pack(fill="x", pady=(0, 14))
        ttk.Label(panel, text="Consulta", style="Campo.TLabel").grid(row=0, column=0, sticky="w")
        self.selector = Selector(panel, [(c, t) for c, (t, _) in self._catalogo.items()],
                                 clave, lambda _: self._preparar(), ancho=70)
        self.selector.grid(row=1, column=0, sticky="w", pady=(3, 0))
        self._etiqueta = ttk.Label(panel, style="Campo.TLabel")
        self._parametro = ttk.Entry(panel, width=14)
        self._parametro.bind("<Return>", lambda _: self._consultar())
        boton(panel, "Ejecutar", "ejecutar", self._consultar, "Primario").grid(
            row=1, column=2, sticky="w", padx=(16, 0), pady=(3, 0))

        self._titulo = ttk.Label(self, style="Subtitulo.TLabel")
        self._titulo.pack(anchor="w", pady=(0, 6))
        self.tabla = Tabla(self)
        self.tabla.pack(fill="both", expand=True)
        self._contador = ttk.Label(self, style="Contador.TLabel")
        self._contador.pack(anchor="e", pady=(6, 0))

        self._preparar()
        if clave is not None and self._catalogo[clave][1] is None:
            self._consultar()

    def _preparar(self):
        clave = self.selector.valor()
        etiqueta = self._catalogo[clave][1] if clave else None
        if etiqueta:
            self._etiqueta.configure(text=etiqueta.capitalize())
            self._etiqueta.grid(row=0, column=1, sticky="w", padx=(16, 0))
            self._parametro.grid(row=1, column=1, sticky="w", padx=(16, 0), pady=(3, 0))
            self._parametro.delete(0, "end")
            self._parametro.insert(0, "1")
        else:
            self._etiqueta.grid_remove()
            self._parametro.grid_remove()

    def _consultar(self):
        clave = self.selector.valor()
        if clave is None:
            return
        parametro = self._parametro.get() if self._catalogo[clave][1] else None
        ok, resultado = ejecutar(self, lambda: self.controlador.ejecutar(clave, parametro))
        if not ok:
            return
        filas = resultado["filas"]
        claves = list(filas[0].keys()) if filas else []
        self.tabla.columnas([(c, e, 160) for c, e in zip(claves, resultado["encabezados"])])
        total = self.tabla.cargar((i, tuple(f.values())) for i, f in enumerate(filas))
        self._titulo.configure(text=resultado["titulo"])
        self._contador.configure(text=f"{total} registros")
