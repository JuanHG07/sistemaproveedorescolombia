"""Punto de entrada de la aplicacion."""
import tkinter as tk
from vista.login_vista import LoginVista


def main():
    raiz = tk.Tk()
    LoginVista(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
