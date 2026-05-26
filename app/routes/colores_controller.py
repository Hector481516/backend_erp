import json
import logging
from app.databases.database import ejecutar_insert
from fastapi import APIRouter, Depends, HTTPException, requests
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.encoders import jsonable_encoder
from typing import Optional, Dict
import os, jsonschema
from jsonschema import validate
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.utils import crear_logg
from app.esquemas.colores import actualiza_color, consulta_colores, eliminar_color
from app.esquemas.schemas import ColorCreate, ColorUpdate

logger = logging.getLogger()
nivel_debug=os.getenv("LOG_LEVEL")
if nivel_debug=='DEBUG':
    logger.setLevel(logging.DEBUG)
elif nivel_debug=='INFO':
    logger.setLevel(logging.INFO)
elif nivel_debug=='WARNING':
    logger.setLevel(logging.WARNING)
elif nivel_debug=='ERROR':
    logger.setLevel(logging.ERROR)
elif nivel_debug=='CRITICAL':
    logger.setLevel(logging.CRITICAL)
if os.getenv("DESACTIVAR_LOGGER"):
    logger.disabled = os.getenv("DESACTIVAR_LOGGER")
else:
    logger.disabled = False
file_handler = logging.FileHandler("./"+os.getenv("LOG_PATH")+datetime.now().strftime('%d-%m-%Y')+".log")

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

bearer_scheme = HTTPBearer()



security = HTTPBearer()

logger = logging.getLogger()
app = APIRouter(
    tags=["Colores"]
)


@app.get('/get_all_colores')
def get_all_colores():
    filtros= {}
    datos=consulta_colores(filtros)
    return {'records': datos}

@app.patch('/actualiza_color/{id_color}')
def update_color(id_color: int, color: ColorUpdate):
    datos=actualiza_color(id_color, color)
    return {'records': datos}

@app.patch('/borrar_color/{id_color}')
def delete_color(id_color):
    datos=eliminar_color(id_color)
    return {'records': datos}

@app.post('/create_color')
def create_color(Color:ColorCreate):
    query = """
        INSERT INTO color (
            descripcion,
            id_estatus_id
        )
        VALUES (%s, %s)
        RETURNING *
    """
    return ejecutar_insert(
        query,
        (
            Color.nombre_color,
            1
        )
    )
