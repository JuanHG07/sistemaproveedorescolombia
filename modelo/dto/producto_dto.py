from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductoDTO:
    """DTO de la tabla producto."""
    id_producto: Optional[object] = None
    codigo: Optional[object] = None
    nombre: Optional[object] = None
    descripcion: Optional[object] = None
    unidad_medida: Optional[object] = None
    id_categoria: Optional[object] = None
    estado: Optional[object] = None
