import os
import psycopg2
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from decimal import Decimal

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
def ejecutar_insert(query, values):
    try:
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()
        result = cur.fetchone()
        columns = [
            desc[0]
            for desc in cur.description
        ]
        return dict(
            zip(columns, result)
        )
    except Exception as e:
        conn.rollback()
        print(e)
        return None
    finally:
        if cur:
            cur.close()
def ejecutar_query(query, values=None, debug=False):
    try:
        cur = conn.cursor()
        if debug:
            print(cur.mogrify(query, values).decode("utf-8"))
        cur.execute(query, values)
        rows = cur.fetchall()
        columns = [
            desc[0]
            for desc in cur.description
        ]
        results = []
        for row in rows:
            row_dict = {}
            for i, value in enumerate(row):
                # datetime -> string
                if isinstance(value, datetime):
                    value = value.isoformat()
                # Decimal -> float
                elif isinstance(value, Decimal):
                    value = float(value)
                row_dict[columns[i]] = value
            results.append(row_dict)
        return results if results else None
    except ValueError as e:
        print(e)
        conn.close()
        return None
    except psycopg2.InterfaceError as e:
        print(e)
        return None
    
def ejecutar_commit(query, values=None):
    cur = None
    try:
        cur = conn.cursor()
        cur.execute(query, values)
        result = None
        # Si la query tiene RETURNING
        if cur.description:
            row = cur.fetchone()
            columns = [
                desc[0]
                for desc in cur.description
            ]
            result = dict(
                zip(columns, row)
            )
        conn.commit()
        return result
    except Exception as e:
        conn.rollback()
        print(e)
        return None
    finally:
        if cur:
            cur.close()