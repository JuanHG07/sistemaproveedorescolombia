import tkinter as tk
from tkinter import ttk
from controlador import permisos
from controlador.auth_controlador import AuthControlador
from controlador.consulta_controlador import ConsultaControlador
from controlador.sesion import Sesion
from controlador.usuario_controlador import UsuarioControlador
from vista.auditoria.bitacora_vista import BitacoraVista
from vista.auditoria.usuario_vista import UsuarioVista, claves_iguales
from vista.componentes.dialogos import confirmar, ejecutar, informar
from vista.componentes.formulario import Formulario
from vista.componentes.tema import (ACENTO, BLANCO, FONDO, FUENTE, PRIMARIO, PRIMARIO_OSCURO,
                                    TEXTO_CLARO, icono, imagen, maximizar, menu)
from vista.consultas.consulta_vista import ConsultaVista
from vista.entidades.categoria_vista import CategoriaVista
from vista.entidades.ciudad_vista import CiudadVista
from vista.entidades.departamento_vista import DepartamentoVista
from vista.entidades.producto_vista import ProductoVista
from vista.entidades.proveedor_vista import ProveedorVista
from vista.inicio_vista import InicioVista
from vista.reportes.reporte_vista import REPORTES, ReporteVista
from vista.transacciones.proveedor_producto_vista import ProveedorProductoVista


class PrincipalVista:
    def __init__(self, raiz, ingreso, al_cerrar_sesion):
        self.raiz = raiz
        self._al_cerrar_sesion = al_cerrar_sesion
        self._actual = None
        self.escritura = permisos.puede_escribir()
        self.admin = permisos.es_admin()

        raiz.resizable(True, True)
        raiz.minsize(1100, 650)
        maximizar(raiz)
        raiz.protocol("WM_DELETE_WINDOW", self._salir)

        self._modulos = {
            "categorias": ("Categorías", "categoria", CategoriaVista),
            "productos": ("Productos", "producto", ProductoVista),
            "proveedores": ("Proveedores", "proveedor", ProveedorVista),
            "departamentos": ("Departamentos", "departamento", DepartamentoVista),
            "ciudades": ("Ciudades", "ciudad", CiudadVista),
            "proveedor_producto": ("Proveedores y productos", "transaccion", ProveedorProductoVista),
            "consultas": ("Consultas", "consulta", ConsultaVista),
            "reportes": ("Reportes", "reporte", ReporteVista),
            "usuarios": ("Usuarios", "usuarios", UsuarioVista),
            "bitacora": ("Bitácora", "bitacora", BitacoraVista),
        }

        self._crear_menu()
        self.marco = tk.Frame(raiz, bg=FONDO)
        self.marco.pack(fill="both", expand=True)
        self._crear_encabezado()
        self._crear_barra_estado(ingreso)
        self.contenido = ttk.Frame(self.marco)
        self.contenido.pack(fill="both", expand=True)
        self.inicio()

    def _crear_menu(self):
        barra = tk.Menu(self.raiz)
        archivo = menu(barra)
        archivo.add_command(label="Inicio", image=icono("inicio"), compound="left", command=self.inicio)
        archivo.add_command(label="Cambiar mi clave", image=icono("clave"), compound="left",
                            command=self._cambiar_clave)
        archivo.add_separator()
        archivo.add_command(label="Cerrar sesión", image=icono("salir"), compound="left",
                            command=self._cerrar_sesion)
        archivo.add_command(label="Salir", image=icono("cancelar"), compound="left", command=self._salir)
        barra.add_cascade(label="Archivo", menu=archivo)

        entidades = menu(barra)
        for clave in ("categorias", "productos", "proveedores", None, "departamentos", "ciudades"):
            self._agregar(entidades, clave)
        barra.add_cascade(label="Entidades", menu=entidades,
                          state="normal" if self.escritura else "disabled")

        transacciones = menu(barra)
        self._agregar(transacciones, "proveedor_producto")
        barra.add_cascade(label="Transacciones", menu=transacciones,
                          state="normal" if self.escritura else "disabled")

        consultas = menu(barra)
        for clave, titulo, _ in ConsultaControlador().catalogo():
            consultas.add_command(label=titulo, image=icono("consulta"), compound="left",
                                  command=lambda c=clave: self.mostrar("consultas", clave=c))
        barra.add_cascade(label="Consultas", menu=consultas)

        reportes = menu(barra)
        for clave, titulo, _, _ in REPORTES:
            reportes.add_command(label=titulo, image=icono("reporte"), compound="left",
                                 command=lambda c=clave: self.mostrar("reportes", clave=c))
        barra.add_cascade(label="Reportes", menu=reportes)

        auditoria = menu(barra)
        self._agregar(auditoria, "usuarios")
        self._agregar(auditoria, "bitacora")
        barra.add_cascade(label="Auditoría", menu=auditoria,
                          state="normal" if self.admin else "disabled")

        ayuda = menu(barra)
        ayuda.add_command(label="Acerca de SPC", image=icono("ayuda"), compound="left",
                          command=self._acerca_de)
        barra.add_cascade(label="Ayuda", menu=ayuda)
        self.raiz.configure(menu=barra)

    def _agregar(self, submenu, clave):
        if clave is None:
            submenu.add_separator()
            return
        titulo, nombre_icono, _ = self._modulos[clave]
        submenu.add_command(label=titulo, image=icono(nombre_icono), compound="left",
                            command=lambda: self.mostrar(clave))

    def _crear_encabezado(self):
        encabezado = tk.Frame(self.marco, bg=PRIMARIO, padx=22, pady=10)
        encabezado.pack(fill="x")
        tk.Label(encabezado, image=imagen("logo_40"), bg=PRIMARIO).pack(side="left")
        textos = tk.Frame(encabezado, bg=PRIMARIO)
        textos.pack(side="left", padx=(12, 0))
        tk.Label(textos, text="SPC", bg=PRIMARIO, fg=BLANCO, font=(FUENTE, 14, "bold"),
                 anchor="w").pack(fill="x")
        tk.Label(textos, text="Sistema de Proveedores Colombianos", bg=PRIMARIO, fg=TEXTO_CLARO,
                 font=(FUENTE, 9), anchor="w").pack(fill="x")
        self._modulo = tk.Label(encabezado, bg=PRIMARIO, fg=BLANCO, font=(FUENTE, 12))
        self._modulo.pack(side="right")
        tk.Frame(self.marco, bg=ACENTO, height=3).pack(fill="x")

    def _crear_barra_estado(self, ingreso):
        barra = tk.Frame(self.marco, bg=PRIMARIO_OSCURO, padx=18, pady=5)
        barra.pack(side="bottom", fill="x")
        usuario = Sesion.usuario
        detalle = (f"Usuario: {usuario.nombre_completo} ({usuario.username})     "
                   f"Perfil: {Sesion.tipo}     Ingreso: {ingreso:%d/%m/%Y %I:%M %p}")
        tk.Label(barra, text=detalle, bg=PRIMARIO_OSCURO, fg=TEXTO_CLARO,
                 font=(FUENTE, 9)).pack(side="left")
        ttk.Button(barra, text="Cerrar sesión", image=icono("salir", True), compound="left",
                   style="Peligro.TButton", command=self._cerrar_sesion).pack(side="right")

    def _reemplazar(self, titulo, crear):
        if self._actual is not None:
            self._actual.destroy()
        self._modulo.configure(text=titulo)
        self._actual = crear(self.contenido)
        self._actual.pack(fill="both", expand=True)

    def mostrar(self, modulo, **opciones):
        titulo, _, clase = self._modulos[modulo]
        self._reemplazar(titulo, lambda padre: clase(padre, **opciones))

    def inicio(self):
        accesos = []
        claves = []
        if self.escritura:
            claves += ["categorias", "productos", "proveedores", "proveedor_producto"]
        claves += ["consultas", "reportes"]
        if self.admin:
            claves += ["usuarios", "bitacora"]
        for clave in claves:
            titulo, nombre_icono, _ = self._modulos[clave]
            accesos.append((titulo, nombre_icono, lambda c=clave: self.mostrar(c)))
        self._reemplazar("Inicio", lambda padre: InicioVista(
            padre, Sesion.usuario.nombre_completo, Sesion.tipo, accesos))

    def _cambiar_clave(self):
        controlador = UsuarioControlador()
        formulario = Formulario(self.raiz, "Cambiar mi clave", lambda f: ejecutar(
            f, lambda: controlador.cambiar_mi_password(f.valor("actual"),
                                                       claves_iguales(f)))[0])
        formulario.entrada("actual", "Clave actual", oculto=True)
        formulario.entrada("clave", "Nueva clave", oculto=True)
        formulario.entrada("confirmacion", "Confirmar nueva clave", oculto=True)
        formulario.nota("La clave debe tener al menos 6 caracteres.")
        formulario.mostrar()
        if formulario.guardado:
            informar(self.raiz, "Su clave se actualizó correctamente.")

    def _acerca_de(self):
        informar(self.raiz, "SPC - Sistema de Proveedores Colombianos\n\n"
                            "Proyecto final de Bases de Datos I\nUniversidad del Quindío\n\n"
                            "Juan Sebastián Hernández\nSantiago Ospina Sánchez")

    def _limpiar(self):
        AuthControlador().logout()
        self.raiz.configure(menu="")
        for widget in self.raiz.winfo_children():
            widget.destroy()

    def _cerrar_sesion(self):
        if confirmar(self.raiz, "¿Desea cerrar la sesión?"):
            self._limpiar()
            self._al_cerrar_sesion()

    def _salir(self):
        if confirmar(self.raiz, "¿Desea salir del sistema?"):
            self._limpiar()
            self.raiz.destroy()
