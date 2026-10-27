from dataclasses import dataclass
from typing import Optional


@dataclass
class BitacoraDTO:
    """DTO de la tabla bitacora."""
    id_bitacora: Optional[object] = None
    id_usuario: Optional[object] = None
    fecha_hora_entrada: Optional[object] = None
    fecha_hora_salida: Optional[object] = None
