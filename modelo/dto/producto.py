from dataclasses import dataclass
from typing import Optional


@dataclass
class Producto:
    id_producto: Optional[int] = None
    codigo: str = ""
    nombre: str = ""
    descripcion: Optional[str] = None
    unidad_medida: str = ""
    id_categoria: Optional[int] = None
    estado: str = "A"
