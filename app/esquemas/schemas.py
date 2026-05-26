from pydantic import BaseModel
from typing import List, Optional


class ColorCreate(BaseModel):

    nombre_color: str

class ColorUpdate(BaseModel):

    nombre_color: str

class MarcaCreate(BaseModel):

    nombre_marca: str

class MarcaUpdate(BaseModel):

    nombre_marca: str

class ModeloCreate(BaseModel):

    nombre: str
    modelo: int
    clave: int
    id_clasificacion: int
    id_marca: int
    id_color: int

class TallaCreate(BaseModel):

    nombre_talla: str

class TallaUpdate(BaseModel):

    nombre_talla: str

class ProductoCreate(BaseModel):

    id_modelo_detalle: int
    id_talla: int
    cantidad: int
    precio_compra: float
    precio_venta: float

class CreateVenta(BaseModel):

    id_talla: int
    precio_venta: int

class ProductoFiltros:
    def __init__(
        self,
        estatus: Optional[int] = None
    ):
        self.estatus = estatus