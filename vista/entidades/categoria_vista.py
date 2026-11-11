from controlador.categoria_controlador import CategoriaControlador
from vista.componentes.vista_crud import VistaCrud


class CategoriaVista(VistaCrud):
    titulo = "Categorías"
    descripcion = "Familias en las que se agrupan los productos del catálogo."
    singular = "categoría"
    femenino = True
    columnas = (("nombre", "Nombre", 240), ("descripcion", "Descripción", 520))

    def __init__(self, padre):
        self.controlador = CategoriaControlador()
        super().__init__(padre)

    def obtener_registros(self):
        return self.controlador.listar()

    def clave(self, registro):
        return registro.id_categoria

    def fila(self, registro):
        return registro.nombre, registro.descripcion

    def campos(self, formulario, registro):
        formulario.entrada("nombre", "Nombre", registro and registro.nombre)
        formulario.entrada("descripcion", "Descripción", registro and registro.descripcion)

    def guardar(self, formulario, registro):
        datos = (formulario.valor("nombre"), formulario.valor("descripcion"))
        if registro is None:
            self.controlador.crear(*datos)
        else:
            self.controlador.actualizar(registro.id_categoria, *datos)

    def borrar(self, registro):
        self.controlador.eliminar(registro.id_categoria)
