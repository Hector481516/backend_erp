from fastapi import FastAPI
import os
import app.routes.modelos_controller as modelos_controller

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "Hola mundo con FastAPI 🚀"}

@app.get("/usuarios/{id}")
def obtener_usuario(id: int):
    return {"usuario_id": id}

app.include_router(modelos_controller.app, prefix='/modelos')
