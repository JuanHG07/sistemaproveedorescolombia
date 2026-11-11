from controlador.ciudad_controlador import CiudadControlador
from controlador.departamento_controlador import DepartamentoControlador
from vista.componentes.vista_crud import VistaCrud


class CiudadVista(VistaCrud):
    titulo = "Ciudades"
    descripcion = "Municipios de Colombia, agrupados por departamento."
    singular = "ciudad"
    femenino = True
    columnas = (("nombre", "Nombre", 320), ("departamento", "Departamento", 320))

    def __init__(self, padre):
        self.controlador = CiudadControlador()
        self.departamentos = {}
        super().__init__(padre)

    def obtener_registros(self):
        self.departamentos = {d.id_departamento: d.nombre
                              for d in DepartamentoControlador().listar()}
        return self.controlador.listar()

    def clave(self, registro):
        return registro.id_ciudad

    def fila(self, registro):
        return registro.nombre, self.departamentos.get(registro.id_departamento)

    def campos(self, formulario, registro):
        formulario.entrada("nombre", "Nombre", registro and registro.nombre)
        formulario.selector("departamento", "Departamento", self.departamentos.items(),
                            registro and registro.id_departamento)

    def guardar(self, formulario, registro):
        datos = (formulario.valor("nombre"), formulario.valor("departamento"))
        if registro is None:
            self.controlador.crear(*datos)
        else:
            self.controlador.actualizar(registro.id_ciudad, *datos)

    def borrar(self, registro):
        self.controlador.eliminar(registro.id_ciudad)
