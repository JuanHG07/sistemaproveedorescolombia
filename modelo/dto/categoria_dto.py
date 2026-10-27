from dataclasses import dataclass
from typing import Optional


@dataclass
class CategoriaDTO:
    """DTO de la tabla categoria."""
    id_categoria: Optional[object] = None
    nombre: Optional[object] = None
    descripcion: Optional[object] = None
