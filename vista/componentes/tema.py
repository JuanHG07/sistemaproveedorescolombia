import tkinter as tk
from tkinter import ttk, messagebox
from config.configuracion import RAIZ

TITULO_APP = "SPC - Sistema de Proveedores Colombianos"
FUENTE = "Segoe UI"

PRIMARIO = "#1F4E79"
PRIMARIO_OSCURO = "#16395A"
SECUNDARIO = "#2E75B6"
ACENTO = "#C9A227"
FONDO = "#F4F6F9"
BLANCO = "#FFFFFF"
FILA_ALTERNA = "#EEF3F8"
BORDE = "#D3DCE6"
TEXTO = "#1E2A36"
TEXTO_SUAVE = "#5B6B7B"
TEXTO_CLARO = "#D6E2EE"
PELIGRO = "#B3261E"
PELIGRO_OSCURO = "#8C1D18"
DESHABILITADO = "#9DB3C8"

_RECURSOS = RAIZ / "recursos"
_imagenes = {}


def icono(nombre, claro=False):
    return _cargar(_RECURSOS / "iconos" / f"{nombre}{'_claro' if claro else ''}.png")


def imagen(nombre):
    return _cargar(_RECURSOS / "imagenes" / f"{nombre}.png")


def _cargar(ruta):
    clave = str(ruta)
    if clave not in _imagenes:
        _imagenes[clave] = tk.PhotoImage(file=clave)
    return _imagenes[clave]


def maximizar(ventana):
    try:
        ventana.state("zoomed")
    except tk.TclError:
        ventana.attributes("-zoomed", True)


def restaurar(ventana):
    try:
        ventana.attributes("-zoomed", False)
    except tk.TclError:
        pass
    ventana.state("normal")


def centrar(ventana, ancho, alto, padre=None):
    ventana.update_idletasks()
    if padre is not None:
        x = padre.winfo_rootx() + (padre.winfo_width() - ancho) // 2
        y = padre.winfo_rooty() + (padre.winfo_height() - alto) // 3
    else:
        x = (ventana.winfo_screenwidth() - ancho) // 2
        y = (ventana.winfo_screenheight() - alto) // 3
    ventana.geometry(f"{ancho}x{alto}+{max(x, 0)}+{max(y, 0)}")


def aplicar(raiz):
    raiz.title(TITULO_APP)
    raiz.configure(bg=FONDO)
    raiz.iconphoto(True, imagen("logo_64"), imagen("logo_32"))
    raiz.report_callback_exception = lambda tipo, error, traza: messagebox.showerror(
        TITULO_APP, f"Ocurrió un error inesperado:\n{error}")
    raiz.option_add("*TCombobox*Listbox.font", (FUENTE, 10))
    raiz.option_add("*TCombobox*Listbox.selectBackground", SECUNDARIO)

    estilo = ttk.Style(raiz)
    estilo.theme_use("clam")
    estilo.configure(".", background=FONDO, foreground=TEXTO, font=(FUENTE, 10),
                     bordercolor=BORDE, focuscolor=SECUNDARIO)

    estilo.configure("TFrame", background=FONDO)
    estilo.configure("Tarjeta.TFrame", background=BLANCO, relief="solid", borderwidth=1)
    estilo.configure("Plano.TFrame", background=BLANCO)

    estilo.configure("TLabel", background=FONDO, foreground=TEXTO)
    estilo.configure("Titulo.TLabel", foreground=PRIMARIO, font=(FUENTE, 18, "bold"))
    estilo.configure("Descripcion.TLabel", foreground=TEXTO_SUAVE)
    estilo.configure("Subtitulo.TLabel", foreground=PRIMARIO, font=(FUENTE, 12, "bold"))
    estilo.configure("Contador.TLabel", foreground=TEXTO_SUAVE, font=(FUENTE, 9))
    estilo.configure("Tarjeta.TLabel", background=BLANCO)
    estilo.configure("Seccion.TLabel", background=BLANCO, foreground=PRIMARIO,
                     font=(FUENTE, 12, "bold"))
    estilo.configure("Campo.TLabel", background=BLANCO, foreground=TEXTO,
                     font=(FUENTE, 10, "bold"))
    estilo.configure("Ayuda.TLabel", background=BLANCO, foreground=TEXTO_SUAVE, font=(FUENTE, 9))

    _boton(estilo, "Primario.TButton", SECUNDARIO, BLANCO, PRIMARIO)
    _boton(estilo, "Peligro.TButton", PELIGRO, BLANCO, PELIGRO_OSCURO)
    estilo.configure("Secundario.TButton", background=BLANCO, foreground=PRIMARIO,
                     bordercolor=PRIMARIO, lightcolor=BLANCO, darkcolor=BLANCO,
                     padding=(14, 6), font=(FUENTE, 10))
    estilo.map("Secundario.TButton",
               background=[("pressed", FILA_ALTERNA), ("active", FILA_ALTERNA)],
               lightcolor=[("active", FILA_ALTERNA)], darkcolor=[("active", FILA_ALTERNA)],
               foreground=[("disabled", DESHABILITADO)])
    estilo.configure("Acceso.TButton", background=BLANCO, foreground=PRIMARIO,
                     bordercolor=BORDE, lightcolor=BLANCO, darkcolor=BLANCO,
                     padding=(16, 14), font=(FUENTE, 11, "bold"), anchor="w")
    estilo.map("Acceso.TButton", background=[("active", FILA_ALTERNA)],
               bordercolor=[("active", SECUNDARIO)],
               lightcolor=[("active", FILA_ALTERNA)], darkcolor=[("active", FILA_ALTERNA)])

    for nombre in ("TEntry", "TCombobox"):
        estilo.configure(nombre, fieldbackground=BLANCO, foreground=TEXTO, padding=6,
                         bordercolor=BORDE, lightcolor=BORDE, darkcolor=BORDE,
                         arrowcolor=PRIMARIO, insertcolor=TEXTO)
        estilo.map(nombre, bordercolor=[("focus", SECUNDARIO)],
                   lightcolor=[("focus", SECUNDARIO)],
                   fieldbackground=[("disabled", FONDO), ("readonly", BLANCO)],
                   foreground=[("disabled", TEXTO_SUAVE)],
                   selectbackground=[("readonly", BLANCO)],
                   selectforeground=[("readonly", TEXTO)])

    estilo.configure("TRadiobutton", background=BLANCO, foreground=TEXTO,
                     indicatorcolor=BLANCO, font=(FUENTE, 10))
    estilo.map("TRadiobutton", indicatorcolor=[("selected", SECUNDARIO)],
               background=[("active", BLANCO)])

    estilo.configure("Treeview", background=BLANCO, fieldbackground=BLANCO, foreground=TEXTO,
                     rowheight=30, bordercolor=BORDE, font=(FUENTE, 10))
    estilo.map("Treeview", background=[("selected", SECUNDARIO)],
               foreground=[("selected", BLANCO)])
    estilo.configure("Treeview.Heading", background=PRIMARIO, foreground=BLANCO,
                     relief="flat", padding=(8, 7), font=(FUENTE, 10, "bold"),
                     bordercolor=PRIMARIO_OSCURO, lightcolor=PRIMARIO, darkcolor=PRIMARIO)
    estilo.map("Treeview.Heading", background=[("active", PRIMARIO_OSCURO)])

    for orientacion in ("Vertical", "Horizontal"):
        estilo.configure(f"{orientacion}.TScrollbar", background="#C5D3E2", troughcolor=FONDO,
                         bordercolor=FONDO, arrowcolor=PRIMARIO, lightcolor="#C5D3E2",
                         darkcolor="#C5D3E2")


def _boton(estilo, nombre, fondo, texto, activo):
    estilo.configure(nombre, background=fondo, foreground=texto, bordercolor=fondo,
                     lightcolor=fondo, darkcolor=fondo, padding=(14, 6),
                     font=(FUENTE, 10, "bold"))
    estilo.map(nombre, background=[("disabled", DESHABILITADO), ("pressed", activo), ("active", activo)],
               bordercolor=[("active", activo)], lightcolor=[("active", activo)],
               darkcolor=[("active", activo)])


def menu(padre):
    return tk.Menu(padre, tearoff=0, bg=BLANCO, fg=TEXTO, activebackground=SECUNDARIO,
                   activeforeground=BLANCO, font=(FUENTE, 10), bd=0)


def boton(padre, texto, nombre_icono, comando, estilo="Secundario"):
    claro = estilo in ("Primario", "Peligro")
    return ttk.Button(padre, text=texto, image=icono(nombre_icono, claro), compound="left",
                      style=f"{estilo}.TButton", command=comando)
