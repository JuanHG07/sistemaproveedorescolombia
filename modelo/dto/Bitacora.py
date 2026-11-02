from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Bitacora:
    id_bitacora: Optional[int] = None
    id_usuario: Optional[int] = None
    fecha_hora_entrada: Optional[datetime] = None
    fecha_hora_salida: Optional[datetime] = None