import json
import logging
from fastapi import APIRouter, Depends, HTTPException, requests
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.encoders import jsonable_encoder
from typing import Optional, Dict
import os, jsonschema
from jsonschema import validate
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.utils import crear_logg
from app.esquemas.schemas import ModeloCreate
from app.databases.database import ejecutar_insert
from app.esquemas.modelos import get_all_modelos, consulta_clasificaciones, actualiza_modelo, eliminar_modelo

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
    tags=["Modelos"]
)


@app.get('/get_all_modelos')
def get_modelos():
    filtros= {}
    datos=get_all_modelos(filtros)
    return {'records': datos}
@app.get('/get_all_clasificaciones')
def get_all_clasificaciones():
    datos=consulta_clasificaciones()
    return {'records': datos}
@app.post('/create_modelo')
def create_modelo(modelo: ModeloCreate):
    query = """
        INSERT INTO catalogos_modelo
        (deleted, deleted_by_cascade, created_at, updated_at, descripcion, modelo, id_estatus_id, id_clasificacion_id, id_marca_id)
        VALUES(NULL, false, now(), now() ,%s, %s, 1, %s, %s)
        RETURNING *
    """
    res=ejecutar_insert(
        query,
        (
            modelo.nombre,
            modelo.modelo,
            modelo.id_clasificacion,
            modelo.id_marca,
        )
    )
    if res:
        query = """
            INSERT INTO public.catalogos_modelodetalle
            (deleted, deleted_by_cascade, created_at, updated_at, clave, id_color_id, id_estatus_id, id_modelo_id)
            VALUES(NULL, false, now(), now(), %s, %s, 1, %s)
            RETURNING *
        """
        return ejecutar_insert(
            query,
            (
                modelo.clave,
                modelo.id_color,
                res['id']
            )
        )
    else:
        raise HTTPException(status_code=500, detail="Error al crear el modelo")
    
@app.patch('/actualiza_modelo/{id_modelo}')
def update_modelo(id_modelo: int, modelo: ModeloCreate):
    print(modelo)
    datos=actualiza_modelo(id_modelo, modelo)
    return {'records': datos}
@app.patch('/borrar_modelo/{id_modelo}')
def delete_modelo(id_modelo):
    datos=eliminar_modelo(id_modelo)
    return {'records': datos}