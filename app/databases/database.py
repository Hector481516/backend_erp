import os
import psycopg2
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

ID_POSITION = 0
CVE_POSITION = 1


DB_HOST = os.getenv('SQL_HOST')
DB_PORT = os.getenv('SQL_PORT')
DB_NAME = os.getenv('SQL_DBNAME')
DB_USER = os.getenv('SQL_USER')
DB_PASS = os.getenv('SQL_PASSWORD')

DATABASE_URL = (
    f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
metadata.reflect(bind=engine)

# Conexión a la base de dato
session = SessionLocal()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)

nombre_base_de_datos = os.getenv("SQL_DBNAME")


def set_db(conn):
    return conn[nombre_base_de_datos]
    
def ejecutar_consulta(query):
    with engine.connect() as connection:
        result = connection.execute(query)
        rows = [list(row) for row in result]
    records = __rows_to_dicts(rows)
    return records
def __rows_to_dicts(rows: list):
    records = []
    for values in rows:
        records.append(dict(zip(values)))
    return records
def ejecutar_query_diccionario(query):
    try:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        result_dict_list = []
        for row in rows:
            result_dict = dict(zip([column[0] for column in cur.description], row))
            result_dict_list.append(result_dict)
        return result_dict_list
    except ValueError:
        print(ValueError)
        conn.close()
    except psycopg2.InterfaceError as e:
        print(e)
def ejecutar_query(query):
    try:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        if len(rows)>0:
            return rows
        else:
            return None
    except ValueError:
        print(ValueError)
        conn.close()
        return None
    except psycopg2.InterfaceError as e:
        print(e)