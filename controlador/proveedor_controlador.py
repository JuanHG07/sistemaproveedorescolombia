from controlador.base_controlador import BaseControlador
from modelo.dao.proveedor_dao import ProveedorDAO
from modelo.dto.proveedor import Proveedor
from utilidades import validaciones as v
from utilidades.constantes import ACTIVO
from utilidades.errores import ErrorNegocio


class ProveedorControlador(BaseControlador):
    def __init__(self):
        self.dao = ProveedorDAO()

    def listar(self):
        return self._leer(self.dao.listar)

    def listar_por_ciudad(self, id_ciudad):
        return self._leer(lambda: self.dao.listar_por_ciudad(
            v.entero_positivo(id_ciudad, "ciudad")))

    def obtener(self, id_proveedor):
        return self._leer(lambda: self.dao.obtener_por_id(id_proveedor))

    def crear(self, nit, razon_social, contacto, telefono, correo,
              direccion, id_ciudad, estado=ACTIVO):
        return self._escribir(lambda: self.dao.insertar(self._construir(
            None, nit, razon_social, contacto, telefono, correo, direccion, id_ciudad, estado)))

    def actualizar(self, id_proveedor, nit, razon_social, contacto, telefono,
                   correo, direccion, id_ciudad, estado):
        def accion():
            self._debe_existir(self.dao.obtener_por_id(id_proveedor), "El proveedor")
            self.dao.actualizar(self._construir(
                id_proveedor, nit, razon_social, contacto, telefono,
                correo, direccion, id_ciudad, estado))
        self._escribir(accion)

    def cambiar_estado(self, id_proveedor, estado):
        self._escribir(lambda: self.dao.cambiar_estado(id_proveedor, v.estado(estado)))

    def eliminar(self, id_proveedor):
        def accion():
            if self.dao.eliminar(id_proveedor) == 0:
                raise ErrorNegocio("El proveedor no existe o ya fue eliminado.")
        self._escribir(accion)

    @staticmethod
    def _construir(id_proveedor, nit, razon_social, contacto, telefono,
                   correo, direccion, id_ciudad, estado):
        return Proveedor(
            id_proveedor=id_proveedor,
            nit=v.nit(nit),
            razon_social=v.texto(razon_social, "razón social", 150),
            contacto=v.texto(contacto, "contacto", 100, obligatorio=False),
            telefono=v.telefono(telefono),
            correo=v.correo(correo),
            direccion=v.texto(direccion, "dirección", 200, obligatorio=False),
            id_ciudad=v.entero_positivo(id_ciudad, "ciudad"),
            estado=v.estado(estado))
