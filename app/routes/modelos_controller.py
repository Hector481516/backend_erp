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
from app.esquemas.modelos import consulta_prueba

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


@app.get('/consulta_prueba')
def get_prueba_consulta():
    filtros= {}
    datos=consulta_prueba(filtros)
    return {'records': datos}
