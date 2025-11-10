import os
from typing import Generator
import psycopg
from dotenv import load_dotenv
from fastapi import HTTPException

# Carga las variables de entorno desde el archivo bd.env
load_dotenv("bd.env") 
passwordDB = os.getenv("PASSWORD") 

# URL de conexión específica de tu Supabase
url = f"postgresql://postgres:{passwordDB}@hnnhpbbupfwwsljlrpqv.supabase.co:5432/postgres"

def getCursor() -> Generator[psycopg.Cursor, None, None]:
    """
    Dependencia de FastAPI que gestiona la conexión, commit y rollback.
    """
    conn = None
    cursor = None
    
    try:
        conn = psycopg.connect(url, sslmode="require")
        cursor = conn.cursor()
        
        yield cursor
        
        conn.commit() 
        
    except psycopg.Error as error:
        if conn:
            conn.rollback()
        print(f"Database error occurred: {error}")
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {error}")
        
    except Exception as error:
        if conn:
            conn.rollback() 
        raise error 
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()