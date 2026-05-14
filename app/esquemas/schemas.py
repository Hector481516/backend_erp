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