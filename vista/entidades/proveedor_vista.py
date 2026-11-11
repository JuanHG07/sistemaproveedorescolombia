from controlador.ciudad_controlador import CiudadControlador
from controlador.departamento_controlador import DepartamentoControlador
from controlador.proveedor_controlador import ProveedorControlador
from vista.componentes.formato import ESTADOS, estado
from vista.componentes.vista_crud import VistaCrud


class ProveedorVista(VistaCrud):
    titulo = "Proveedores"
    descripcion = "Empresas de cualquier ciudad de Colombia que abastecen el catálogo."
    singular = "proveedor"
    columnas = (("nit", "NIT", 120), ("razon_social", "Razón social", 240),
                ("ciudad", "Ciudad", 150), ("telefono", "Teléfono", 120),
                ("correo", "Correo", 220), ("estado", "Estado", 90))

    def __init__(self, padre):
        self.controlador = ProveedorControlador()
        self.ciudades = {}
        self.departamentos = {}
        super().__init__(padre)

    def obtener_registros(self):
        self.departamentos = {d.id_departamento: d.nombre
                              for d in DepartamentoControlador().listar()}
        self.ciudades = {c.id_ciudad: c for c in CiudadControlador().listar()}
        return self.controlador.listar()

    def clave(self, registro):
        return registro.id_proveedor

    def fila(self, registro):
        ciudad = self.ciudades.get(registro.id_ciudad)
        return (registro.nit, registro.razon_social, ciudad.nombre if ciudad else "",
                registro.telefono, registro.correo, estado(registro.estado))

    def _ciudades_de(self, id_departamento):
        return [(c.id_ciudad, c.nombre) for c in self.ciudades.values()
                if c.id_departamento == id_departamento]

    def campos(self, formulario, registro):
        ciudad = self.ciudades.get(registro.id_ciudad) if registro else None
        id_departamento = ciudad.id_departamento if ciudad else None
        formulario.entrada("nit", "NIT", registro and registro.nit)
        formulario.entrada("razon_social", "Razón social", registro and registro.razon_social)
        formulario.entrada("contacto", "Persona de contacto", registro and registro.contacto)
        formulario.entrada("telefono", "Teléfono", registro and registro.telefono)
        formulario.entrada("correo", "Correo electrónico", registro and registro.correo)
        formulario.entrada("direccion", "Dirección", registro and registro.direccion)
        formulario.selector("departamento", "Departamento", self.departamentos.items(),
                            id_departamento,
                            lambda valor: formulario.campo("ciudad").opciones(self._ciudades_de(valor)))
        formulario.selector("ciudad", "Ciudad", self._ciudades_de(id_departamento),
                            ciudad and ciudad.id_ciudad)
        formulario.selector("estado", "Estado", ESTADOS, registro.estado if registro else "A")

    def guardar(self, formulario, registro):
        datos = (formulario.valor("nit"), formulario.valor("razon_social"),
                 formulario.valor("contacto"), formulario.valor("telefono"),
                 formulario.valor("correo"), formulario.valor("direccion"),
                 formulario.valor("ciudad"), formulario.valor("estado"))
        if registro is None:
            self.controlador.crear(*datos)
        else:
            self.controlador.actualizar(registro.id_proveedor, *datos)

    def borrar(self, registro):
        self.controlador.eliminar(registro.id_proveedor)
