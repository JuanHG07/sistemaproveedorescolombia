import base64
import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk
import pymupdf
from utilidades.constantes import CARPETA_REPORTES
from vista.componentes.dialogos import informar
from vista.componentes.tema import BORDE, FONDO, TITULO_APP, boton, centrar


class VisorPDF(tk.Toplevel):
    def __init__(self, padre, ruta, titulo):
        super().__init__(padre)
        self.withdraw()
        self.title(f"Vista previa - {titulo}")
        self.configure(bg=FONDO)
        self.transient(padre.winfo_toplevel())
        self._ruta = ruta
        self._documento = pymupdf.open(ruta)
        self._pagina = 0
        self._zoom = 1.2
        self._imagen = None

        barra = ttk.Frame(self, padding=(16, 10))
        barra.pack(fill="x")
        boton(barra, "", "anterior", lambda: self._ir(-1)).pack(side="left")
        self._indicador = ttk.Label(barra, width=16, anchor="center")
        self._indicador.pack(side="left", padx=6)
        boton(barra, "", "siguiente", lambda: self._ir(1)).pack(side="left")
        boton(barra, "", "alejar", lambda: self._escalar(-0.2)).pack(side="left", padx=(18, 0))
        self._escala = ttk.Label(barra, width=6, anchor="center")
        self._escala.pack(side="left", padx=6)
        boton(barra, "", "acercar", lambda: self._escalar(0.2)).pack(side="left")
        boton(barra, "Cerrar", "cancelar", self.cerrar).pack(side="right")
        boton(barra, "Guardar PDF", "pdf", self._guardar, "Primario").pack(side="right", padx=(0, 8))

        marco = ttk.Frame(self)
        marco.pack(fill="both", expand=True)
        self._lienzo = tk.Canvas(marco, bg=BORDE, highlightthickness=0)
        vertical = ttk.Scrollbar(marco, orient="vertical", command=self._lienzo.yview)
        horizontal = ttk.Scrollbar(marco, orient="horizontal", command=self._lienzo.xview)
        self._lienzo.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        self._lienzo.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)
        self._lienzo.bind("<Configure>", lambda _: self._ubicar())
        self._lienzo.bind("<MouseWheel>", lambda e: self._lienzo.yview_scroll(-e.delta // 120, "units"))
        self._lienzo.bind("<Button-4>", lambda _: self._lienzo.yview_scroll(-1, "units"))
        self._lienzo.bind("<Button-5>", lambda _: self._lienzo.yview_scroll(1, "units"))

        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.bind("<Escape>", lambda _: self.cerrar())
        self.bind("<Left>", lambda _: self._ir(-1))
        self.bind("<Right>", lambda _: self._ir(1))

    def mostrar(self):
        alto = min(self.winfo_screenheight() - 120, 900)
        centrar(self, min(self.winfo_screenwidth() - 80, 1180), alto)
        self.deiconify()
        self._dibujar()
        self.grab_set()
        self.focus_set()

    def _dibujar(self):
        pagina = self._documento[self._pagina]
        mapa = pagina.get_pixmap(matrix=pymupdf.Matrix(self._zoom, self._zoom))
        self._imagen = tk.PhotoImage(data=base64.b64encode(mapa.tobytes("png")).decode("ascii"))
        self._indicador.configure(text=f"Página {self._pagina + 1} de {self._documento.page_count}")
        self._escala.configure(text=f"{round(self._zoom * 100)}%")
        self._lienzo.delete("all")
        self._lienzo.create_image(0, 20, image=self._imagen, anchor="n", tags="pagina")
        self._ubicar()
        self._lienzo.yview_moveto(0)

    def _ubicar(self):
        if self._imagen is None:
            return
        ancho = max(self._lienzo.winfo_width(), self._imagen.width() + 40)
        self._lienzo.coords("pagina", ancho / 2, 20)
        self._lienzo.configure(scrollregion=(0, 0, ancho, self._imagen.height() + 40))

    def _ir(self, paso):
        destino = self._pagina + paso
        if 0 <= destino < self._documento.page_count:
            self._pagina = destino
            self._dibujar()

    def _escalar(self, paso):
        zoom = round(self._zoom + paso, 1)
        if 0.6 <= zoom <= 2.4:
            self._zoom = zoom
            self._dibujar()

    def _guardar(self):
        os.makedirs(CARPETA_REPORTES, exist_ok=True)
        destino = filedialog.asksaveasfilename(
            parent=self, title=TITULO_APP, defaultextension=".pdf",
            filetypes=[("Documento PDF", "*.pdf")], initialdir=CARPETA_REPORTES,
            initialfile=os.path.basename(self._ruta))
        if destino:
            shutil.copyfile(self._ruta, destino)
            informar(self, f"El reporte se guardó en:\n{destino}")

    def cerrar(self):
        self._documento.close()
        try:
            os.remove(self._ruta)
        except OSError:
            pass
        self.destroy()
