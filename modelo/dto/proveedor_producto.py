from dataclasses import dataclass
from typing import Optional


@dataclass
class ProveedorProducto:
    id_proveedor: Optional[int] = None
    id_producto: Optional[int] = None
    precio_unitario: Optional[float] = None
    dias_entrega: Optional[int] = None
