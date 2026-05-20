from fastapi import APIRouter, UploadFile, File

from app.services.carga_masiva_service import (
    cargar_modelos_excel,
    cargar_productos_excel
)

app = APIRouter()

@app.post('/Alta-Masiva')
async def carga_masiva_modelos(
    file: UploadFile = File(...)
):

    return await cargar_modelos_excel(file)


@app.post('/productos')
async def carga_masiva_productos(
    file: UploadFile = File(...)
):

    return await cargar_productos_excel(file)