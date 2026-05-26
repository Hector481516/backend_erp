from app.esquemas.schemas import ColorUpdate
from fastapi.encoders import jsonable_encoder
from app.databases.database import ejecutar_consulta, ejecutar_query_diccionario, ejecutar_query
import json, logging, os
from datetime import datetime
from app.utils.utils import crear_logg
from fastapi import HTTPException
from app.databases.database import ejecutar_commit

def consulta_tallas(filtros):
    try:
        query=f'''
             SELECT to_char(talla.created_at,'DD-MM-YYYY')creacion,to_char(talla.updated_at,'DD-MM-YYYY')actualizacion,id as id_talla,descripcion as nombre_talla, 
                (select est.descripcion from  estatus est where est.id=talla.id_estatus_id) estatus 
            FROM talla talla
            ORDER BY talla.descripcion;'''
        # datos=ejecutar_query_diccionario(query)
        datos=ejecutar_query(query)
        listado_json= json.loads(json.dumps(datos))
        return jsonable_encoder(listado_json)
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'pedimento.py','pedimentos')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
    
def consulta_talla_by_descripcion(descripcion):
    try:
        query=f'''
             SELECT to_char(tall.created_at,'DD-MM-YYYY')creacion,to_char(tall.updated_at,'DD-MM-YYYY')actualizacion,id as id_talla,descripcion as nombre_talla, 
                (select est.descripcion from  estatus est where est.id=tall.id_estatus_id) estatus 
            FROM talla tall
            WHERE tall.descripcion='{descripcion}'
            ORDER BY tall.descripcion;'''
        datos=ejecutar_query(query)
        listado_json= json.loads(json.dumps(datos))
        return jsonable_encoder(listado_json)
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'marcas.py','marcas')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
    
def consulta_tallas_by_modelo(filtros):
    try:
        query=f'''
            SELECT tall.id id_talla, tall.descripcion as talla
            FROM producto cp
            INNER JOIN talla tall on tall.id=cp.id_talla_id 
            WHERE cp.id_modelo_detalle_id ={filtros.get('id_modelo_detalle')}
            GROUP BY tall.id, tall.descripcion'''
        datos=ejecutar_query(query)
        listado_json= json.loads(json.dumps(datos))
        return jsonable_encoder(listado_json)
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'marcas.py','marcas')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")