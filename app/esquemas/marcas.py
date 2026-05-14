from app.esquemas.schemas import MarcaUpdate
from fastapi.encoders import jsonable_encoder
from app.databases.database import ejecutar_consulta, ejecutar_query_diccionario, ejecutar_query
import json, logging, os
from datetime import datetime
from app.utils.utils import crear_logg
from fastapi import HTTPException
from app.databases.database import ejecutar_commit

def consulta_marcas(filtros):
    try:
        query=f'''
             SELECT to_char(mar.created_at,'DD-MM-YYYY')creacion,to_char(mar.updated_at,'DD-MM-YYYY')actualizacion,id as id_marca,descripcion as nombre_marca, 
                (select est.descripcion from  catalogos_estatus est where est.id=mar.id_estatus_id) estatus 
            FROM catalogos_marca mar
            ORDER BY mar.descripcion;'''
        datos=ejecutar_query(query)
        listado_json= json.loads(json.dumps(datos))
        return jsonable_encoder(listado_json)
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'marcas.py','marcas')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
    
def actualiza_marcas(id_marca: int, marca: MarcaUpdate):
    try:
        query = """
            UPDATE catalogos_marca
            SET descripcion = %s
            WHERE id = %s
            RETURNING *
        """
        values = (marca.nombre_marca, id_marca)
        resultado = ejecutar_commit(query, values)
        return resultado
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'marcas.py','marcas')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
    
def eliminar_marca(id_marca):
    try:
        query = """
            UPDATE catalogos_marca
            SET id_estatus_id = 3
            WHERE id = %s
            RETURNING *
        """
        values = (id_marca)
        resultado = ejecutar_commit(query, values)
        print(resultado)
        return resultado
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'marcas.py','marcas')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")