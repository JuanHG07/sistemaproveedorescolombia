from dataclasses import dataclass
from typing import Optional


@dataclass
class ProveedorProductoDTO:
    """DTO de la tabla proveedor_producto (clave compuesta)."""
    id_proveedor: Optional[int] = None
    id_producto: Optional[int] = None
    precio_unitario: Optional[float] = None
    dias_entrega: Optional[int] = None
