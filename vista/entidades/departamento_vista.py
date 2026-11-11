from controlador.departamento_controlador import DepartamentoControlador
from vista.componentes.vista_crud import VistaCrud


class DepartamentoVista(VistaCrud):
    titulo = "Departamentos"
    descripcion = "Divisiones territoriales de Colombia donde se ubican los proveedores."
    singular = "departamento"
    columnas = (("nombre", "Nombre", 400),)

    def __init__(self, padre):
        self.controlador = DepartamentoControlador()
        super().__init__(padre)

    def obtener_registros(self):
        return self.controlador.listar()

    def clave(self, registro):
        return registro.id_departamento

    def fila(self, registro):
        return (registro.nombre,)

    def campos(self, formulario, registro):
        formulario.entrada("nombre", "Nombre", registro and registro.nombre)

    def guardar(self, formulario, registro):
        if registro is None:
            self.controlador.crear(formulario.valor("nombre"))
        else:
            self.controlador.actualizar(registro.id_departamento, formulario.valor("nombre"))

    def borrar(self, registro):
        self.controlador.eliminar(registro.id_departamento)
