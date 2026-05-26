import json
import logging
from app.esquemas.modelos import actualiza_modelo, consulta_clasificaciones, eliminar_modelo, eliminar_modelo
from fastapi import APIRouter, Depends, HTTPException, requests
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.encoders import jsonable_encoder
from typing import List, Optional, Dict
import os, jsonschema
from jsonschema import validate
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.utils import crear_logg
from app.esquemas.schemas import ModeloCreate, ProductoCreate, CreateVenta, ProductoFiltros
from app.esquemas.productos import get_all_productos, actualiza_producto, eliminar_producto, get_tallas_by_modelo_detalle, insertar_productos, actualiza_marcar_venta

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
    tags=["Productos"]
)


@app.get('/get_all_productos')
def get_productos( filtros: ProductoFiltros=Depends()):
    print(filtros)
    return {'records': get_all_productos(filtros)}

# @app.get('/get_all_productos')
# def get_productos_catalogos(filtros):
#     filtros= {}
#     datos=get_all_productos(filtros)
#     productos = {}
#     for row in datos:
#         id_modelo_detalle_id = row['id_modelo_detalle']
#         tallas=get_tallas_by_modelo_detalle(id_modelo_detalle_id)
#         if id_modelo_detalle_id not in productos:
#             row["tallas"] = tallas
#     return {'records': datos}

@app.post('/create_producto')
def create_producto( productos: List[ProductoCreate]):
    res= insertar_productos(productos)
    return {'message': 'Productos creados exitosamente'}

@app.patch('/actualiza_producto/{id_producto}')
def update_producto(id_producto: int, producto: ModeloCreate):
    datos=actualiza_producto(id_producto, producto)
    return {'records': datos}

@app.patch('/borrar_producto/{id_producto}')
def delete_producto(id_producto: int):
    datos=eliminar_producto(id_producto)
    return {'records': datos}

@app.patch('/marcar_venta/{id_modelo_detalle}')
def marcar_venta(id_modelo_detalle: int, producto: CreateVenta):
    datos=actualiza_marcar_venta(id_modelo_detalle, producto)
    return {'records': datos}