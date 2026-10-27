from dataclasses import dataclass
from typing import Optional


@dataclass
class TipoUsuarioDTO:
    """DTO de la tabla tipo_usuario."""
    id_tipo: Optional[object] = None
    nombre: Optional[object] = None
