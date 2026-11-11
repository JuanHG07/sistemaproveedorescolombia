import tempfile
import tkinter as tk
from tkinter import ttk
from controlador.categoria_controlador import CategoriaControlador
from controlador.ciudad_controlador import CiudadControlador
from controlador.departamento_controlador import DepartamentoControlador
from controlador.producto_controlador import ProductoControlador
from controlador.proveedor_controlador import ProveedorControlador
from controlador.reporte_controlador import ReporteControlador
from controlador.sesion import Sesion
from utilidades.generador_pdf import generar_pdf
from vista.componentes.dialogos import ejecutar
from vista.componentes.formato import ESTADOS
from vista.componentes.selector import Selector
from vista.componentes.tema import boton
from vista.componentes.visor_pdf import VisorPDF

REPORTES = (
    ("proveedores_por_ubicacion", "Proveedores por ubicación",
     "Proveedores según su departamento, ciudad y estado.", ("departamento", "ciudad", "estado")),
    ("proveedores_de_producto", "Proveedores por producto",
     "Proveedores que suministran un producto, con precio y días de entrega.", ("producto",)),
    ("productos_de_proveedor", "Productos por proveedor",
     "Productos que ofrece un proveedor, con su categoría y precio.", ("proveedor",)),
    ("productos_por_categoria", "Productos por categoría",
     "Productos de una categoría según su estado.", ("categoria", "estado")),
    ("resumen_por_categoria", "Resumen por categoría",
     "Cantidad de productos, proveedores y precio promedio por categoría.", ("categoria",)),
)

FILTROS = {
    "departamento": ("Departamento", "id_departamento"),
    "ciudad": ("Ciudad", "id_ciudad"),
    "estado": ("Estado", "estado"),
    "producto": ("Producto", "id_producto"),
    "proveedor": ("Proveedor", "id_proveedor"),
    "categoria": ("Categoría", "id_categoria"),
}

TODOS = (None, "Todos")


class ReporteVista(ttk.Frame):
    def __init__(self, padre, clave=REPORTES[0][0]):
        super().__init__(padre, padding=(28, 22))
        self.controlador = ReporteControlador()
        self._reporte = tk.StringVar(value=clave)
        self._selectores = {}
        self._opciones = {}

        ttk.Label(self, text="Reportes", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(self, text="Elija un reporte, ajuste los filtros y revise la vista previa antes de guardarlo en PDF.",
                  style="Descripcion.TLabel").pack(anchor="w", pady=(2, 14))

        cuerpo = ttk.Frame(self)
        cuerpo.pack(fill="both", expand=True)
        lista = ttk.Frame(cuerpo, style="Tarjeta.TFrame", padding=(18, 14))
        lista.pack(side="left", fill="y")
        ttk.Label(lista, text="Reporte", style="Seccion.TLabel").pack(anchor="w", pady=(0, 8))
        for clave_reporte, titulo, descripcion, _ in REPORTES:
            ttk.Radiobutton(lista, text=titulo, value=clave_reporte, variable=self._reporte,
                            command=self._preparar).pack(anchor="w", pady=(6, 0))
            ttk.Label(lista, text=descripcion, style="Ayuda.TLabel", wraplength=300).pack(
                anchor="w", padx=(22, 0))

        lateral = ttk.Frame(cuerpo, style="Tarjeta.TFrame", padding=(22, 14))
        lateral.pack(side="left", fill="both", expand=True, padx=(14, 0))
        ttk.Label(lateral, text="Filtros", style="Seccion.TLabel").pack(anchor="w")
        ttk.Label(lateral, text="Deje un filtro en \"Todos\" para no aplicarlo.",
                  style="Ayuda.TLabel").pack(anchor="w", pady=(0, 6))
        self._filtros = ttk.Frame(lateral, style="Plano.TFrame")
        self._filtros.pack(fill="x")
        boton(lateral, "Generar vista previa", "reporte", self._generar, "Primario").pack(
            anchor="w", pady=(18, 0))

        if self._cargar_opciones():
            self._preparar()

    def _cargar_opciones(self):
        def cargar():
            return {
                "departamento": [(d.id_departamento, d.nombre) for d in DepartamentoControlador().listar()],
                "producto": [(p.id_producto, f"{p.codigo} - {p.nombre}") for p in ProductoControlador().listar()],
                "proveedor": [(p.id_proveedor, p.razon_social) for p in ProveedorControlador().listar()],
                "categoria": [(c.id_categoria, c.nombre) for c in CategoriaControlador().listar()],
                "estado": list(ESTADOS),
                "ciudad": [],
            }
        ok, opciones = ejecutar(self, cargar)
        if ok:
            self._opciones = opciones
        return ok

    def _definicion(self):
        return next(r for r in REPORTES if r[0] == self._reporte.get())

    def _preparar(self):
        for widget in self._filtros.winfo_children():
            widget.destroy()
        self._selectores = {}
        for fila, nombre in enumerate(self._definicion()[3]):
            etiqueta, _ = FILTROS[nombre]
            ttk.Label(self._filtros, text=etiqueta, style="Campo.TLabel").grid(
                row=fila * 2, column=0, sticky="w", pady=(10, 3))
            al_cambiar = self._cambio_departamento if nombre == "departamento" else None
            selector = Selector(self._filtros, [TODOS] + self._opciones.get(nombre, []),
                                al_cambiar=al_cambiar, ancho=48)
            selector.grid(row=fila * 2 + 1, column=0, sticky="w")
            self._selectores[nombre] = selector

    def _cambio_departamento(self, id_departamento):
        ciudades = []
        if id_departamento is not None:
            ok, lista = ejecutar(self, lambda: CiudadControlador().listar_por_departamento(id_departamento))
            ciudades = [(c.id_ciudad, c.nombre) for c in lista] if ok else []
        self._selectores["ciudad"].opciones([TODOS] + ciudades)

    def _generar(self):
        clave, titulo, _, _ = self._definicion()
        argumentos = {FILTROS[n][1]: s.valor() for n, s in self._selectores.items()}

        def generar():
            datos = getattr(self.controlador, clave)(**argumentos)
            usuario = Sesion.usuario.username if Sesion.usuario else ""
            return generar_pdf(datos["titulo"], datos["encabezados"], datos["filas"], clave,
                               datos["filtros"], tempfile.gettempdir(), usuario)

        ok, ruta = ejecutar(self, generar)
        if ok:
            VisorPDF(self, ruta, titulo).mostrar()
