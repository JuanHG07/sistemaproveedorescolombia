from tkinter import ttk
from vista.componentes.tema import FUENTE, icono, imagen


class InicioVista(ttk.Frame):
    def __init__(self, padre, nombre, perfil, accesos):
        super().__init__(padre, padding=(28, 22))
        tarjeta = ttk.Frame(self, style="Tarjeta.TFrame", padding=(32, 26))
        tarjeta.pack(fill="x")
        ttk.Label(tarjeta, image=imagen("logo_128"), style="Tarjeta.TLabel").grid(
            row=0, column=0, rowspan=3, padx=(0, 28))
        ttk.Label(tarjeta, text=f"Bienvenido(a), {nombre}", style="Seccion.TLabel",
                  font=(FUENTE, 18, "bold")).grid(row=0, column=1, sticky="sw")
        ttk.Label(tarjeta, text=f"Perfil: {perfil}", style="Tarjeta.TLabel").grid(
            row=1, column=1, sticky="w")
        ttk.Label(tarjeta, text="Use el menú superior o los accesos directos para trabajar con la información.",
                  style="Ayuda.TLabel").grid(row=2, column=1, sticky="nw", pady=(4, 0))

        ttk.Label(self, text="Accesos directos", style="Subtitulo.TLabel").pack(anchor="w", pady=(24, 10))
        rejilla = ttk.Frame(self)
        rejilla.pack(fill="x")
        for i, (texto, nombre_icono, comando) in enumerate(accesos):
            ttk.Button(rejilla, text=f"  {texto}", image=icono(nombre_icono), compound="left",
                       style="Acceso.TButton", command=comando).grid(
                row=i // 4, column=i % 4, sticky="ew", padx=(0, 12), pady=(0, 12))
        for columna in range(4):
            rejilla.columnconfigure(columna, weight=1, uniform="accesos")
