from app.routes import productos_controller
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import app.routes.modelos_controller as modelos_controller
import app.routes.colores_controller as colores_controller
import app.routes.marcas_controller as marcas_controller
import app.routes.tallas_controller as tallas_controller
from fastapi.staticfiles import StaticFiles

import os

ruta = "C:/calzado"

print(os.listdir(ruta))

app = FastAPI()
app.mount(
    "/imagenes",
    # StaticFiles(directory="C:\\Users\\Hecto\\OneDrive\\Imágenes\\Imagenes zapatos\\Calzado marketplace"),
    StaticFiles(directory="C:\\calzado"),
    name="imagenes"
)

@app.get("/")
def read_root():
    return {"mensaje": "Hola mundo con FastAPI 🚀"}

@app.get("/usuarios/{id}")
def obtener_usuario(id: int):
    return {"usuario_id": id}

app.include_router(modelos_controller.app, prefix='/modelos')
app.include_router(colores_controller.app, prefix='/colores')
app.include_router(marcas_controller.app, prefix='/marcas')
app.include_router(productos_controller.app, prefix='/productos')
app.include_router(tallas_controller.app, prefix='/tallas')
origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
