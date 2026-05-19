from pydantic import BaseModel


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