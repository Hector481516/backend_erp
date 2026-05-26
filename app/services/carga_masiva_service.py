import pandas as pd
from io import BytesIO
from app.databases.database import ejecutar_insert
from app.esquemas.marcas import consulta_marcas_by_descripcion
from app.esquemas.clasificacion import consulta_clasificacion_by_descripcion
from app.esquemas.colores import consulta_color_by_descripcion
from app.esquemas.productos import get_modelo_detalle_by_clave
from app.esquemas.tallas import consulta_talla_by_descripcion



async def cargar_modelos_excel(file):
    contenido = await file.read()
    df = pd.read_excel(
        BytesIO(contenido)
    )
    registros_insertados = 0
    contador=0
    for _, row in df.iterrows():
        contador+=1
        query = """
        INSERT INTO modelo
        (deleted, deleted_by_cascade, created_at, updated_at, descripcion, modelo, id_estatus_id, id_clasificacion_id, id_marca_id)
        VALUES(NULL, false, now(), now() ,%s, %s, 1, %s, %s)
        RETURNING *
        """
        marca=consulta_marcas_by_descripcion(row.Marca)[0]
        clasificacion=consulta_clasificacion_by_descripcion(row.Tipo_prenda)[0]
        res=ejecutar_insert(
            query,
            (
                row.Descripcion,
                row.Modelo,
                clasificacion['id_clasificacion'],
                marca['id_marca']
            )
        )
        if res:
            color=consulta_color_by_descripcion(row.Color)[0]
            query = """
                INSERT INTO public.modelo_detalle
                (deleted, deleted_by_cascade, created_at, updated_at, clave, id_color_id, id_estatus_id, id_modelo_id)
                VALUES(NULL, false, now(), now(), %s, %s, 1, %s)
                """
            valores = (
                row['Codigo'],
                color['id_color'],
                res['id']
            )
            ejecutar_insert(query, valores)
            registros_insertados += 1
    return {
        "ok": True,
        "insertados": registros_insertados
    }

def limpiar_numero(valor):

    if isinstance(valor, float) and valor.is_integer():
        return int(valor)

    return valor

async def cargar_productos_excel(file):
    contenido = await file.read()
    df = pd.read_excel(
        BytesIO(contenido)
    )
    contador=0
    for _, row in df.iterrows():
        contador+=1
        query = """
            INSERT INTO producto
                (deleted, deleted_by_cascade, created_at, updated_at, precio_venta, id_modelo_detalle_id, id_estatus_id, id_talla_id, precio_compra)
                VALUES(NULL, false, now(), now() ,%s, %s, 1, %s, %s)
        """
        clave=row.Modelo.split(" ")[-1]
        talla=consulta_talla_by_descripcion(limpiar_numero(row['Talla']))[0]
        id_modelo_detalle=get_modelo_detalle_by_clave(clave)[0]
        ejecutar_insert(
            query,
            (
                row['Precio_venta'],
                id_modelo_detalle['id_modelo_detalle'],
                talla['id_talla'],
                row['Precio_compra']
            )
        )
    # return {
    #     "ok": True
    # }