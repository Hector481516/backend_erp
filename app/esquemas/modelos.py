from fastapi.encoders import jsonable_encoder
from app.databases.database import ejecutar_consulta, ejecutar_query_diccionario, ejecutar_query
import json, logging, os
from datetime import datetime
from app.utils.utils import crear_logg
from fastapi import HTTPException
def consulta_prueba(filtros):
    try:
        query=f'''
            SELECT observaciones FROM catalogos_compra'''
        # datos=ejecutar_query_diccionario(query)
        datos=ejecutar_query(query)
        listado_json= json.loads(json.dumps(datos))
        return jsonable_encoder(listado_json)
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'pedimento.py','pedimentos')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")