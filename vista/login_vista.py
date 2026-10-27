import tkinter as tk
from tkinter import ttk, messagebox
from controlador.auth_controlador import AuthControlador


class LoginVista:
    def __init__(self, raiz):
        self.raiz = raiz
        self.auth = AuthControlador()
        raiz.title("Ingreso al sistema")
        raiz.geometry("340x200")
        raiz.resizable(False, False)

        marco = ttk.Frame(raiz, padding=20)
        marco.pack(expand=True)
        ttk.Label(marco, text="Usuario").grid(row=0, column=0, sticky="w", pady=4)
        self.e_user = ttk.Entry(marco, width=25)
        self.e_user.grid(row=0, column=1)
        ttk.Label(marco, text="Clave").grid(row=1, column=0, sticky="w", pady=4)
        self.e_clave = ttk.Entry(marco, width=25, show="*")
        self.e_clave.grid(row=1, column=1)
        ttk.Button(marco, text="Ingresar", command=self.ingresar).grid(row=2, column=0, columnspan=2, pady=14)
        self.e_user.focus()
        raiz.bind("<Return>", lambda e: self.ingresar())

    def ingresar(self):
        try:
            self.auth.login(self.e_user.get(), self.e_clave.get())
        except Exception as ex:
            messagebox.showerror("Error", str(ex))
            return
        self.raiz.destroy()
        from vista.principal_vista import PrincipalVista
        PrincipalVista(self.auth).iniciar()
