import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=os.getenv("PGPORT", "5432"),
        database=os.getenv("PGDATABASE", "agendamento_salas"),
        user=os.getenv("PGUSER", "miguelangelo"),
        password=os.getenv("PGPASSWORD", "")
    )
