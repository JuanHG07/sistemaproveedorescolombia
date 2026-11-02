from dataclasses import dataclass
from typing import Optional


@dataclass
class Usuario:
    id_usuario: Optional[int] = None
    nombre_completo: str = ""
    username: str = ""
    password_hash: str = ""
    id_tipo: Optional[int] = None
    estado: str = "A"