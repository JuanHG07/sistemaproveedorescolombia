from dataclasses import dataclass
from typing import Optional


@dataclass
class DepartamentoDTO:
    """DTO de la tabla departamento."""
    id_departamento: Optional[object] = None
    nombre: Optional[object] = None
