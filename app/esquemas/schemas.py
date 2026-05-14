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
    modelo: str
    clave: str
    clasificacion: int
    marca: int
    color: int