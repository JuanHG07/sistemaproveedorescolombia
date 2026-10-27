from dataclasses import dataclass
from typing import Optional


@dataclass
class UsuarioDTO:
    """DTO de la tabla usuario."""
    id_usuario: Optional[object] = None
    nombre_completo: Optional[object] = None
    username: Optional[object] = None
    password_hash: Optional[object] = None
    id_tipo: Optional[object] = None
    estado: Optional[object] = None
