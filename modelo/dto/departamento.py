from dataclasses import dataclass
from typing import Optional


@dataclass
class Departamento:
    id_departamento: Optional[int] = None
    nombre: str = ""
