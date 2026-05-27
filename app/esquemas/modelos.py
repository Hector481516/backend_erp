from fastapi.encoders import jsonable_encoder
from app.databases.database import ejecutar_consulta, ejecutar_query_diccionario, ejecutar_query
import json, logging, os
from datetime import datetime
from app.utils.utils import crear_logg
from fastapi import HTTPException
from app.databases.database import ejecutar_commit
def get_all_modelos(filtros):
    try:
        query='''
            SELECT to_char(mod.created_at,'DD-MM-YYYY')creacion,mod.id AS id_modelo,mod.descripcion,mod.modelo AS numero_modelo, clas.descripcion AS clasificacion,det.clave,det.path_imagen as imagen,
	            col.descripcion as color, clas.descripcion as clasificacion, mar.descripcion as marca, col.id AS id_color, CLAS.id AS id_clasificacion, mar.id AS id_marca, det.id AS id_modelo_detalle
            FROM  modelo mod
            INNER JOIN modelo_detalle det ON det.id_modelo_id=mod.id
            INNER JOIN clasificacion clas ON clas.id=mod.id_clasificacion_id
            INNER JOIN color col ON col.id=det.id_color_id
            INNER JOIN marca mar ON mar.id=mod.id_marca_id'''
        where = []
        params = {}
        if filtros.estatus is not None:
            where.append("mod.id_estatus_id = %(estatus)s")
            params["estatus"] = filtros.estatus
        if where:
            query += " AND " + " AND ".join(where)
        query+='''
            ORDER BY mar.descripcion, mod.descripcion;'''
        # datos=ejecutar_query_diccionario(query)
        datos=ejecutar_query(query)
        listado_json= json.loads(json.dumps(datos))
        return jsonable_encoder(listado_json)
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'pedimento.py','pedimentos')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
    
def consulta_clasificaciones():
    try:
        query=f'''
            SELECT id as id_clasificacion,descripcion as clasificacion
            FROM clasificacion clas ;'''
        # datos=ejecutar_query_diccionario(query)
        datos=ejecutar_query(query)
        listado_json= json.loads(json.dumps(datos))
        return jsonable_encoder(listado_json)
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'pedimento.py','pedimentos')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")

def actualiza_modelo(id_modelo: int, modelo):
    try:
        query = """
            UPDATE modelo
            SET descripcion = %s, modelo = %s, id_clasificacion_id = %s, id_marca_id = %s
            WHERE id = %s
            RETURNING *
        """
        values = (modelo.nombre, modelo.modelo, modelo.id_clasificacion, modelo.id_marca, id_modelo)
        resultado = ejecutar_commit(query, values)
        if resultado:
            query_detalle = """
                UPDATE modelo_detalle
                SET clave = %s, id_color_id = %s
                WHERE id_modelo_id = %s
                RETURNING *
            """
            values_detalle = (modelo.clave, modelo.id_color, id_modelo)
            resultado_detalle = ejecutar_commit(query_detalle, values_detalle)
            if resultado_detalle:
                return resultado_detalle
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'marcas.py','marcas')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
def eliminar_modelo(id_modelo):
    try:
        query = """
            UPDATE modelo
            SET id_estatus_id = 3
            WHERE id = %s
            RETURNING *
        """
        values = (id_modelo)
        resultado = ejecutar_commit(query, values)
        return resultado
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'marcas.py','marcas')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")