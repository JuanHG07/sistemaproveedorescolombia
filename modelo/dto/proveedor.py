from dataclasses import dataclass
from typing import Optional


@dataclass
class Proveedor:
    id_proveedor: Optional[int] = None
    nit: str = ""
    razon_social: str = ""
    contacto: Optional[str] = None
    telefono: str = ""
    correo: Optional[str] = None
    direccion: Optional[str] = None
    id_ciudad: Optional[int] = None
    estado: str = "A"