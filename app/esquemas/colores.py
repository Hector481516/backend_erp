from app.esquemas.schemas import ColorUpdate
from fastapi.encoders import jsonable_encoder
from app.databases.database import ejecutar_consulta, ejecutar_query_diccionario, ejecutar_query
import json, logging, os
from datetime import datetime
from app.utils.utils import crear_logg
from fastapi import HTTPException
from app.databases.database import ejecutar_commit

def consulta_colores(filtros):
    try:
        query=f'''
             SELECT to_char(col.created_at,'DD-MM-YYYY')creacion,to_char(col.updated_at,'DD-MM-YYYY')actualizacion,id as id_color,descripcion as nombre_color, 
                (select est.descripcion from  catalogos_estatus est where est.id=col.id_estatus_id) estatus 
            FROM catalogos_color col
            ORDER BY col.descripcion;'''
        # datos=ejecutar_query_diccionario(query)
        datos=ejecutar_query(query)
        listado_json= json.loads(json.dumps(datos))
        return jsonable_encoder(listado_json)
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'pedimento.py','pedimentos')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
    
def consulta_color_by_descripcion(descripcion):
    try:
        query=f'''
             SELECT to_char(col.created_at,'DD-MM-YYYY')creacion,to_char(col.updated_at,'DD-MM-YYYY')actualizacion,id as id_color,descripcion as nombre_color, 
                (select est.descripcion from  catalogos_estatus est where est.id=col.id_estatus_id) estatus 
            FROM catalogos_color col
            WHERE col.descripcion='{descripcion}'
            ORDER BY col.descripcion;'''
        datos=ejecutar_query(query)
        listado_json= json.loads(json.dumps(datos))
        return jsonable_encoder(listado_json)
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'marcas.py','marcas')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
    
def actualiza_color(id_color: int, color: ColorUpdate):
    try:
        query = """
            UPDATE catalogos_color
            SET descripcion = %s
            WHERE id = %s
            RETURNING *
        """
        values = (color.nombre_color, id_color)
        resultado = ejecutar_commit(query, values)
        return resultado
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'colores.py','colores')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
    
def eliminar_color(id_color):
    try:
        query = """
            UPDATE catalogos_color
            SET id_estatus_id = 3
            WHERE id = %s
            RETURNING *
        """
        values = (id_color)
        resultado = ejecutar_commit(query, values)
        print(resultado)
        return resultado
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'colores.py','colores')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")