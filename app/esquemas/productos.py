from fastapi.encoders import jsonable_encoder
from app.databases.database import ejecutar_consulta, ejecutar_query_diccionario, ejecutar_query
import json, logging, os
from datetime import datetime
from app.utils.utils import crear_logg
from fastapi import HTTPException
from app.databases.database import ejecutar_commit
from app.databases.database import ejecutar_insert

def get_tallas_by_modelo_detalle(id_modelo_detalle):
    try:
        query="""
            SELECT tall.descripcion as talla, count(tall.id) cantidad, tall.id as id_talla
            FROM  producto prod
            INNER JOIN talla tall on tall.id=prod.id_talla_id
            INNER JOIN modelo_detalle det on det.id=prod.id_modelo_detalle_id 
            WHERE prod.id_modelo_detalle_id =%s
            AND prod.id_estatus_id=1
            GROUP BY prod.id_modelo_detalle_id,tall.descripcion, tall.id
            ORDER BY tall.id;"""
        # datos=ejecutar_query_diccionario(query)
        datos=ejecutar_query(query, [id_modelo_detalle])
        listado_json= json.loads(json.dumps(datos))
        return jsonable_encoder(listado_json)
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'pedimento.py','pedimentos')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
    
def get_all_productos(filtros):
    try:
        query='''
            SELECT to_char(det.created_at,'DD-MM-YYYY')creacion, 
                mod.descripcion, 
                clas.descripcion AS clasificacion,
                det.clave,
                prod.precio_venta, 
                prod.precio_compra,
                col.descripcion as color, 
                clas.descripcion as clasificacion,
                mar.descripcion as marca, 
                col.id AS id_color, 
                clas.id AS id_clasificacion, 
                mar.id AS id_marca,
                prod.id_modelo_detalle_id as id_modelo_detalle, 
                det.path_imagen as imagen, 
                det.id, 
                count(prod.id) as cantidad_total
            FROM producto prod  
            INNER JOIN modelo_detalle det ON prod.id_modelo_detalle_id=det.id
            INNER JOIN modelo mod ON det.id_modelo_id=mod.id
            INNER JOIN clasificacion clas ON clas.id=mod.id_clasificacion_id
            INNER JOIN color col ON col.id=det.id_color_id
            INNER JOIN marca mar ON mar.id=mod.id_marca_id
            WHERE 1=1
            '''
        where = []
        params = {}
        if filtros.estatus is not None:
            where.append("prod.id_estatus_id = %(estatus)s")
            params["estatus"] = filtros.estatus
        if where:
            query += " AND " + " AND ".join(where)
        query += '''
            GROUP by det.id, mod.descripcion, clas.descripcion,det.clave,prod.precio_venta, prod.precio_compra,
            col.descripcion, clas.descripcion, mar.descripcion, col.id , clas.id, mar.id,
            prod.id_modelo_detalle_id, det.path_imagen, det.id;'''
        datos=ejecutar_query(query,params)
        productos = {}
        for row in datos:
            id_modelo_detalle_id = row['id_modelo_detalle']
            tallas=get_tallas_by_modelo_detalle(id_modelo_detalle_id)
            if id_modelo_detalle_id not in productos:
                row["tallas"] = tallas
            row['imagen']=os.getenv("VITE_PATH_IMAGENES_CALZADO")+row['imagen']
        listado_json= json.loads(json.dumps(datos))
        return jsonable_encoder(listado_json)
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'pedimento.py','pedimentos')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
    

def actualiza_producto(id_producto: int, producto):
    try:
        query = """
            UPDATE modelo
            SET descripcion = %s, modelo = %s, id_clasificacion_id = %s, id_marca_id = %s
            WHERE id = %s
            RETURNING *
        """
        values = (producto.nombre, producto.modelo, producto.id_clasificacion, producto.id_marca, id_producto)
        resultado = ejecutar_commit(query, values)
        if resultado:
            query_detalle = """
                UPDATE modelo_detalle
                SET clave = %s, id_color_id = %s
                WHERE id_modelo_id = %s
                RETURNING *
            """
            values_detalle = (producto.clave, producto.id_color, id_producto)
            resultado_detalle = ejecutar_commit(query_detalle, values_detalle)
            if resultado_detalle:
                return resultado_detalle
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'productos.py','productos')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
def eliminar_producto(id_producto):
    try:
        query = """
            UPDATE modelo
            SET id_estatus_id = 3
            WHERE id = %s
            RETURNING *
        """
        values = (id_producto)
        resultado = ejecutar_commit(query, values)
        return resultado
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'marcas.py','marcas')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
def insertar_productos(productos):
    for producto in productos:
        for _ in range(producto.cantidad):
            query = """
                INSERT INTO producto
                (deleted, deleted_by_cascade, created_at, updated_at, precio_venta, id_modelo_detalle_id, id_estatus_id, id_talla_id, precio_compra)
                VALUES(NULL, false, now(), now() ,%s, %s, 1, %s, %s)
                RETURNING *
            """
            print(f"Insertando producto: {producto}")
            try:
                ejecutar_insert(
                    query,
                    (
                        producto.precio_venta,
                        producto.id_modelo_detalle,
                        producto.id_talla,
                        producto.precio_compra
                    )
                )
                print(f"Producto creado exitosamente: {producto}")
            except Exception as e:
                print(f"An error occurred: {e}")
                crear_logg('error', f"Ocurrió un error: {e}",'productos.py','productos')
                raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
    return {'message': 'Producto creado exitosamente'}

def get_modelo_detalle_by_clave(clave):
    try:
        query=f'''
            SELECT id as id_modelo_detalle 
            FROM modelo_detalle 
            WHERE clave={clave};'''
        datos=ejecutar_query(query)
        listado_json= json.loads(json.dumps(datos))
        return jsonable_encoder(listado_json)
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'marcas.py','marcas')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")
def actualiza_marcar_venta(id_modelo_detalle, producto):
    try:
        query = """
            WITH registro AS (
                SELECT id
                FROM producto
                WHERE id_modelo_detalle_id= %s
                AND id_talla_id=%s
                ORDER BY created_at asc
                LIMIT 1
            )
            UPDATE producto
            SET precio_venta = %s, id_estatus_id=5
            WHERE id IN (
                SELECT id FROM registro
            );
        """
        values = (id_modelo_detalle,producto.id_talla, producto.precio_venta)
        print(values)
        resultado = ejecutar_commit(query, values)
        return resultado
    except Exception as e:
        print(f"An error occurred: {e}")
        crear_logg('error', f"Ocurrió un error: {e}",'marcas.py','marcas')
        raise HTTPException(status_code=500, detail=f"Ocurrió un error: {e}")