from dataclasses import dataclass
from typing import Optional


@dataclass
class Ciudad:
    id_ciudad: Optional[int] = None
    nombre: str = ""
    id_departamento: Optional[int] = None