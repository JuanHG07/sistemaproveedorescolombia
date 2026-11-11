from controlador.bitacora_controlador import BitacoraControlador
from vista.componentes.vista_crud import VistaCrud


class BitacoraVista(VistaCrud):
    titulo = "Bitácora de accesos"
    descripcion = "Registro de las fechas y horas de entrada y salida de cada usuario."
    solo_lectura = True
    columnas = (("usuario", "Usuario", 140), ("nombre", "Nombre completo", 240),
                ("tipo", "Perfil", 130), ("entrada", "Entrada", 200), ("salida", "Salida", 200))

    def __init__(self, padre):
        self.controlador = BitacoraControlador()
        super().__init__(padre)

    def obtener_registros(self):
        return self.controlador.listar()

    def clave(self, registro):
        return registro["id_bitacora"]

    def fila(self, registro):
        return (registro["username"], registro["nombre_completo"], registro["tipo"],
                registro["fecha_hora_entrada"], registro["fecha_hora_salida"] or "Sesión abierta")
