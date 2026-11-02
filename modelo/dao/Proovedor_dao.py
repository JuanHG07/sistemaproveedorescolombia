from typing import List, Optional
from modelo.dao.base_dao import BaseDAO
from modelo.dto.proveedor import Proveedor


class ProveedorDAO(BaseDAO):
    _COLS = ("id_proveedor, nit, razon_social, contacto, telefono, "
             "correo, direccion, id_ciudad, estado")

    def insertar(self, p: Proveedor) -> int:
        sql = ("INSERT INTO proveedor (nit, razon_social, contacto, telefono, correo, "
               "direccion, id_ciudad, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        return self._insertar(sql, (p.nit, p.razon_social, p.contacto, p.telefono,
                                    p.correo, p.direccion, p.id_ciudad, p.estado))

    def listar(self) -> List[Proveedor]:
        filas = self._consultar(f"SELECT {self._COLS} FROM proveedor ORDER BY razon_social")
        return [Proveedor(**f) for f in filas]

    def listar_por_ciudad(self, id_ciudad: int) -> List[Proveedor]:
        filas = self._consultar(
            f"SELECT {self._COLS} FROM proveedor WHERE id_ciudad = %s ORDER BY razon_social",
            (id_ciudad,))
        return [Proveedor(**f) for f in filas]

    def obtener_por_id(self, id_proveedor: int) -> Optional[Proveedor]:
        fila = self._consultar_uno(
            f"SELECT {self._COLS} FROM proveedor WHERE id_proveedor = %s", (id_proveedor,))
        return Proveedor(**fila) if fila else None

    def obtener_por_nit(self, nit: str) -> Optional[Proveedor]:
        fila = self._consultar_uno(
            f"SELECT {self._COLS} FROM proveedor WHERE nit = %s", (nit,))
        return Proveedor(**fila) if fila else None

    def actualizar(self, p: Proveedor) -> int:
        sql = ("UPDATE proveedor SET nit = %s, razon_social = %s, contacto = %s, telefono = %s, "
               "correo = %s, direccion = %s, id_ciudad = %s, estado = %s WHERE id_proveedor = %s")
        return self._ejecutar(sql, (p.nit, p.razon_social, p.contacto, p.telefono, p.correo,
                                    p.direccion, p.id_ciudad, p.estado, p.id_proveedor))

    def cambiar_estado(self, id_proveedor: int, estado: str) -> int:
        return self._ejecutar("UPDATE proveedor SET estado = %s WHERE id_proveedor = %s",
                              (estado, id_proveedor))

    def eliminar(self, id_proveedor: int) -> int:
        return self._ejecutar("DELETE FROM proveedor WHERE id_proveedor = %s", (id_proveedor,))