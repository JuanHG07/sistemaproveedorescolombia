from dataclasses import dataclass
from typing import Optional


@dataclass
class CiudadDTO:
    """DTO de la tabla ciudad."""
    id_ciudad: Optional[object] = None
    nombre: Optional[object] = None
    id_departamento: Optional[object] = None
