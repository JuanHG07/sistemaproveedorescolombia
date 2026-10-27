import tkinter as tk
from tkinter import messagebox
from controlador.sesion import Sesion
from controlador import permisos


class PrincipalVista:
    """Ventana principal con menu segun el tipo de usuario."""

    def __init__(self, auth):
        self.auth = auth
        self.raiz = tk.Tk()
        self.raiz.title(f"Proveedores y Productos - {Sesion.usuario.username} ({Sesion.tipo})")
        self.raiz.geometry("1100x650")
        self.raiz.protocol("WM_DELETE_WINDOW", self.salir)  # registra salida al cerrar
        self._menu()

    def _menu(self):
        barra = tk.Menu(self.raiz)

        archivo = tk.Menu(barra, tearoff=0)
        archivo.add_command(label="Cerrar sesion", command=self.cerrar_sesion)
        archivo.add_command(label="Salir", command=self.salir)
        barra.add_cascade(label="Archivo", menu=archivo)

        estado = "normal" if permisos.puede_escribir() else "disabled"
        entidades = tk.Menu(barra, tearoff=0)
        for txt in ("Categorias", "Productos", "Proveedores", "Departamentos y ciudades"):
            entidades.add_command(label=txt, state=estado, command=lambda t=txt: self.abrir(t))
        barra.add_cascade(label="Entidades", menu=entidades)

        trans = tk.Menu(barra, tearoff=0)
        trans.add_command(label="Productos por proveedor", state=estado, command=lambda: self.abrir("Transacciones"))
        barra.add_cascade(label="Transacciones", menu=trans)

        cons = tk.Menu(barra, tearoff=0)
        cons.add_command(label="Consultas", command=lambda: self.abrir("Consultas"))
        barra.add_cascade(label="Consultas", menu=cons)

        rep = tk.Menu(barra, tearoff=0)
        rep.add_command(label="Reportes", command=lambda: self.abrir("Reportes"))
        barra.add_cascade(label="Reportes", menu=rep)

        if permisos.es_admin():
            aud = tk.Menu(barra, tearoff=0)
            aud.add_command(label="Usuarios", command=lambda: self.abrir("Usuarios"))
            aud.add_command(label="Bitacora", command=lambda: self.abrir("Bitacora"))
            barra.add_cascade(label="Auditoria", menu=aud)

        self.raiz.config(menu=barra)

    def abrir(self, modulo):
        # TODO: instanciar la vista de cada modulo (Toplevel/Frame dentro de la ventana MDI)
        messagebox.showinfo("En construccion", f"Modulo: {modulo}")

    def cerrar_sesion(self):
        self.auth.logout()
        self.raiz.destroy()
        import tkinter as tk2
        from vista.login_vista import LoginVista
        nueva = tk2.Tk()
        LoginVista(nueva)
        nueva.mainloop()

    def salir(self):
        self.auth.logout()
        self.raiz.destroy()

    def iniciar(self):
        self.raiz.mainloop()
