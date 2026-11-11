from controlador.producto_controlador import ProductoControlador
from controlador.proveedor_controlador import ProveedorControlador
from controlador.proveedor_producto_controlador import ProveedorProductoControlador
from utilidades.constantes import ACTIVO
from vista.componentes.vista_crud import VistaCrud


class ProveedorProductoVista(VistaCrud):
    titulo = "Proveedores y productos"
    descripcion = "Productos que suministra cada proveedor, con su precio y tiempo de entrega."
    singular = "asignación"
    femenino = True
    columnas = (("proveedor", "Proveedor", 240), ("codigo", "Código", 100),
                ("producto", "Producto", 260), ("precio", "Precio unitario", 140),
                ("dias", "Días de entrega", 130))

    def __init__(self, padre):
        self.controlador = ProveedorProductoControlador()
        self.proveedores = []
        self.productos = []
        super().__init__(padre)

    def obtener_registros(self):
        self.proveedores = ProveedorControlador().listar()
        self.productos = ProductoControlador().listar()
        return self.controlador.listar_detallado()

    def clave(self, registro):
        return f"{registro['id_proveedor']}-{registro['id_producto']}"

    def fila(self, registro):
        return (registro["proveedor"], registro["codigo"], registro["producto"],
                registro["precio_unitario"], registro["dias_entrega"])

    def campos(self, formulario, registro):
        nuevo = registro is None
        proveedores = [(p.id_proveedor, f"{p.razon_social} ({p.nit})") for p in self.proveedores
                       if not nuevo or p.estado == ACTIVO]
        productos = [(p.id_producto, f"{p.codigo} - {p.nombre}") for p in self.productos
                     if not nuevo or p.estado == ACTIVO]
        formulario.selector("proveedor", "Proveedor", proveedores,
                            registro and registro["id_proveedor"], habilitado=nuevo)
        formulario.selector("producto", "Producto", productos,
                            registro and registro["id_producto"], habilitado=nuevo)
        formulario.entrada("precio", "Precio unitario", registro and registro["precio_unitario"])
        formulario.entrada("dias", "Días de entrega", registro and registro["dias_entrega"])
        if nuevo:
            formulario.nota("Solo se muestran proveedores y productos activos.")

    def guardar(self, formulario, registro):
        datos = (formulario.valor("proveedor"), formulario.valor("producto"),
                 formulario.valor("precio"), formulario.valor("dias"))
        if registro is None:
            self.controlador.asignar(*datos)
        else:
            self.controlador.actualizar(*datos)

    def borrar(self, registro):
        self.controlador.quitar(registro["id_proveedor"], registro["id_producto"])
