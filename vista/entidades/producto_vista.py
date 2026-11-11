from controlador.categoria_controlador import CategoriaControlador
from controlador.producto_controlador import ProductoControlador
from vista.componentes.formato import ESTADOS, estado
from vista.componentes.vista_crud import VistaCrud


class ProductoVista(VistaCrud):
    titulo = "Productos"
    descripcion = "Catálogo de artículos que pueden pedirse a los proveedores."
    singular = "producto"
    columnas = (("codigo", "Código", 110), ("nombre", "Nombre", 280),
                ("categoria", "Categoría", 180), ("unidad", "Unidad de medida", 150),
                ("estado", "Estado", 100))

    def __init__(self, padre):
        self.controlador = ProductoControlador()
        self.categorias = {}
        super().__init__(padre)

    def obtener_registros(self):
        self.categorias = {c.id_categoria: c.nombre for c in CategoriaControlador().listar()}
        return self.controlador.listar()

    def clave(self, registro):
        return registro.id_producto

    def fila(self, registro):
        return (registro.codigo, registro.nombre, self.categorias.get(registro.id_categoria),
                registro.unidad_medida, estado(registro.estado))

    def campos(self, formulario, registro):
        formulario.entrada("codigo", "Código", registro and registro.codigo)
        formulario.entrada("nombre", "Nombre", registro and registro.nombre)
        formulario.entrada("descripcion", "Descripción", registro and registro.descripcion)
        formulario.entrada("unidad", "Unidad de medida", registro and registro.unidad_medida)
        formulario.selector("categoria", "Categoría", self.categorias.items(),
                            registro and registro.id_categoria)
        formulario.selector("estado", "Estado", ESTADOS, registro.estado if registro else "A")

    def guardar(self, formulario, registro):
        datos = (formulario.valor("codigo"), formulario.valor("nombre"),
                 formulario.valor("descripcion"), formulario.valor("unidad"),
                 formulario.valor("categoria"), formulario.valor("estado"))
        if registro is None:
            self.controlador.crear(*datos)
        else:
            self.controlador.actualizar(registro.id_producto, *datos)

    def borrar(self, registro):
        self.controlador.eliminar(registro.id_producto)
