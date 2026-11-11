import tkinter as tk
from datetime import datetime
from tkinter import ttk
from controlador.auth_controlador import AuthControlador
from vista.componentes.dialogos import ejecutar
from vista.componentes.tema import (ACENTO, BLANCO, FUENTE, PRIMARIO, TEXTO_CLARO, TEXTO_SUAVE,
                                    aplicar, centrar, icono, imagen, restaurar)
from vista.principal_vista import PrincipalVista


class LoginVista:
    ANCHO = 440
    ALTO = 620

    def __init__(self, raiz):
        self.raiz = raiz
        aplicar(raiz)
        restaurar(raiz)
        raiz.resizable(False, False)
        raiz.minsize(self.ANCHO, self.ALTO)
        centrar(raiz, self.ANCHO, self.ALTO)
        raiz.protocol("WM_DELETE_WINDOW", raiz.destroy)
        self.controlador = AuthControlador()

        self.marco = tk.Frame(raiz, bg=BLANCO)
        self.marco.pack(fill="both", expand=True)

        encabezado = tk.Frame(self.marco, bg=PRIMARIO, pady=26)
        encabezado.pack(fill="x")
        tk.Label(encabezado, image=imagen("logo_128"), bg=PRIMARIO).pack()
        tk.Label(encabezado, text="Sistema de Proveedores Colombianos", bg=PRIMARIO, fg=BLANCO,
                 font=(FUENTE, 14, "bold")).pack(pady=(12, 0))
        tk.Label(encabezado, text="Gestión de proveedores, productos y categorías",
                 bg=PRIMARIO, fg=TEXTO_CLARO, font=(FUENTE, 9)).pack()
        tk.Frame(self.marco, bg=ACENTO, height=4).pack(fill="x")

        formulario = ttk.Frame(self.marco, style="Plano.TFrame", padding=(44, 24, 44, 0))
        formulario.pack(fill="x")
        formulario.columnconfigure(0, weight=1)
        ttk.Label(formulario, text="Iniciar sesión", style="Seccion.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        ttk.Label(formulario, text="Usuario", style="Campo.TLabel").grid(
            row=1, column=0, columnspan=2, sticky="w", pady=(0, 3))
        self.usuario = ttk.Entry(formulario)
        self.usuario.grid(row=2, column=0, columnspan=2, sticky="ew")
        ttk.Label(formulario, text="Clave", style="Campo.TLabel").grid(
            row=3, column=0, columnspan=2, sticky="w", pady=(12, 3))
        self.clave = ttk.Entry(formulario, show="•")
        self.clave.grid(row=4, column=0, sticky="ew")
        ttk.Button(formulario, image=icono("ojo"), style="Secundario.TButton",
                   command=self._alternar_clave).grid(row=4, column=1, padx=(6, 0), sticky="ns")
        ttk.Button(formulario, text="Ingresar", image=icono("usuario", True), compound="left",
                   style="Primario.TButton", command=self._ingresar).grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=(22, 0), ipady=4)

        tk.Label(self.marco, text="Universidad del Quindío · Bases de Datos I", bg=BLANCO,
                 fg=TEXTO_SUAVE, font=(FUENTE, 8)).pack(side="bottom", pady=12)

        raiz.bind("<Return>", lambda _: self._ingresar())
        self.usuario.focus_set()

    def _alternar_clave(self):
        self.clave.configure(show="" if self.clave.cget("show") else "•")

    def _ingresar(self):
        ok, _ = ejecutar(self.raiz, lambda: self.controlador.login(self.usuario.get(), self.clave.get()))
        if not ok:
            self.clave.delete(0, "end")
            self.clave.focus_set()
            return
        self.raiz.unbind("<Return>")
        self.marco.destroy()
        PrincipalVista(self.raiz, datetime.now(), lambda: LoginVista(self.raiz))
