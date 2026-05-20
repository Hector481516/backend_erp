from app.esquemas.schemas import MarcaUpdate
from fastapi.encoders import jsonable_encoder
from app.databases.database import ejecutar_consulta, ejecutar_query_diccionario, ejecutar_query
import json, logging, os
from datetime import datetime
from app.utils.utils import crear_logg
from fastapi import HTTPException
from app.databases.database import ejecutar_commit

def consulta_clasificacion_by_descripcion(descripcion):
    try:
        query=f'''
             SELECT to_char(clas.created_at,'DD-MM-YYYY')creacion,to_char(clas.updated_at,'DD-MM-YYYY')actualizacion,id as id_clasificacion,descripcion as nombre_clasificacion, 
                (select est.descripcion from  catalogos_estatus est where est.id=clas.id_estatus_id) estatus 
            FROM catalogos_clasificacion clas
            WHERE clas.descripcion='{descripcion}'
            ORDER BY clas.descripcion;'''
        datos=ejecutar_query(query)
        listado_json= json.loads(json.dumps(datos))
        return jsonable_encoder(listado_json)
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'marcas.py','marcas')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
