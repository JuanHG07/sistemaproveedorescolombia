from dataclasses import dataclass
from typing import Optional


@dataclass
class Categoria:
    id_categoria: Optional[int] = None
    nombre: str = ""
    descripcion: Optional[str] = None