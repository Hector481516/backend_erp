import os, logging
from datetime import datetime

def crear_logg(nivel: str, mensaje: str, endpoint: str, controlador:str):
    # Obtener la ruta del log desde la variable de entorno
    log_dir = os.getenv("LOG_PATH", "/tmp") + f"/{controlador}/{endpoint}/"
    # Crear el directorio si no existe
    os.makedirs(log_dir, exist_ok=True)
    # Definir el archivo de log
    log_file = os.path.join(log_dir, datetime.now().strftime('%d-%m-%Y') + ".log")
    # Crear un logger exclusivo para este endpoint
    logger = logging.getLogger(endpoint)
    logger.setLevel(logging.DEBUG)  # Asegurar que se capturen todos los niveles
    # Evitar añadir múltiples handlers al logger (previene duplicación de logs)
    if not logger.handlers:
        print(log_file)
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    # Convertir el nivel de string a un valor de logging
    nivel_log = getattr(logging, nivel.upper(), logging.ERROR)
    # Registrar el mensaje en el log
    logger.log(nivel_log, mensaje)
    # Cerrar el handler para liberar el archivo (opcional en algunos casos)
    file_handler.close()
    logger.removeHandler(file_handler)