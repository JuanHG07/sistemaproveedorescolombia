from tkinter import ttk
from controlador import permisos
from vista.componentes.dialogos import confirmar, ejecutar, informar
from vista.componentes.formulario import Formulario
from vista.componentes.tabla import Tabla
from vista.componentes.tema import boton, icono


class VistaCrud(ttk.Frame):
    titulo = ""
    descripcion = ""
    singular = ""
    femenino = False
    columnas = ()
    solo_lectura = False
    permite_eliminar = True

    def __init__(self, padre):
        super().__init__(padre, padding=(28, 22))
        self.escritura = permisos.puede_escribir() and not self.solo_lectura
        self._registros = {}

        ttk.Label(self, text=self.titulo, style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(self, text=self.descripcion, style="Descripcion.TLabel").pack(anchor="w", pady=(2, 14))

        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(0, 10))
        if self.escritura:
            boton(barra, f"{'Nueva' if self.femenino else 'Nuevo'}", "agregar",
                  lambda: self._abrir(None), "Primario").pack(side="left")
            boton(barra, "Editar", "editar", self._editar).pack(side="left", padx=(8, 0))
            if self.permite_eliminar:
                boton(barra, "Eliminar", "eliminar", self._eliminar).pack(side="left", padx=(8, 0))
        self.acciones_extra(barra)
        boton(barra, "Actualizar", "actualizar", self.recargar).pack(side="left", padx=(8, 0))

        self._busqueda = ttk.Entry(barra, width=32)
        self._busqueda.pack(side="right")
        self._busqueda.bind("<KeyRelease>", lambda _: self._filtrar())
        ttk.Label(barra, image=icono("buscar")).pack(side="right", padx=(0, 6))

        self.tabla = Tabla(self, self.columnas, self._editar if self.escritura else None)
        self.tabla.pack(fill="both", expand=True)
        self._contador = ttk.Label(self, style="Contador.TLabel")
        self._contador.pack(anchor="e", pady=(6, 0))
        self.recargar()

    def obtener_registros(self):
        return []

    def clave(self, registro):
        return ""

    def fila(self, registro):
        return ()

    def campos(self, formulario, registro):
        pass

    def guardar(self, formulario, registro):
        pass

    def borrar(self, registro):
        pass

    def acciones_extra(self, barra):
        pass

    def recargar(self):
        ok, registros = ejecutar(self, self.obtener_registros)
        if not ok:
            return
        self._registros = {str(self.clave(r)): r for r in registros}
        self._mostrar_total(self.tabla.cargar((self.clave(r), self.fila(r)) for r in registros))

    def _filtrar(self):
        self._mostrar_total(self.tabla.filtrar(self._busqueda.get()))

    def _mostrar_total(self, visibles):
        total = len(self._registros)
        self._contador.configure(text=f"{visibles} de {total} registros" if visibles != total
                                 else f"{total} registros")

    def seleccionado(self):
        iid = self.tabla.seleccionado()
        if iid is None:
            informar(self, "Seleccione un registro de la tabla.")
            return None
        return self._registros.get(iid)

    def _editar(self):
        registro = self.seleccionado()
        if registro is not None:
            self._abrir(registro)

    def _abrir(self, registro):
        articulo = "Nueva" if self.femenino else "Nuevo"
        titulo = f"Editar {self.singular}" if registro is not None else f"{articulo} {self.singular}"
        formulario = Formulario(self, titulo, lambda f: ejecutar(f, lambda: self.guardar(f, registro))[0])
        self.campos(formulario, registro)
        formulario.mostrar()
        if formulario.guardado:
            self.recargar()

    def _eliminar(self):
        registro = self.seleccionado()
        if registro is None:
            return
        articulo, terminacion = ("la", "a") if self.femenino else ("el", "o")
        if not confirmar(self, f"¿Desea eliminar {articulo} {self.singular} seleccionad{terminacion}?"):
            return
        ok, _ = ejecutar(self, lambda: self.borrar(registro))
        if ok:
            self.recargar()
