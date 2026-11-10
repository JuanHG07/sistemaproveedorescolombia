from dataclasses import dataclass
from typing import Optional


@dataclass
class TipoUsuario:
    id_tipo: Optional[int] = None
    nombre: str = ""
