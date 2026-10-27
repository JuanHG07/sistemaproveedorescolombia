from dataclasses import dataclass
from typing import Optional


@dataclass
class ProveedorDTO:
    """DTO de la tabla proveedor."""
    id_proveedor: Optional[object] = None
    nit: Optional[object] = None
    razon_social: Optional[object] = None
    contacto: Optional[object] = None
    telefono: Optional[object] = None
    correo: Optional[object] = None
    direccion: Optional[object] = None
    id_ciudad: Optional[object] = None
    estado: Optional[object] = None
