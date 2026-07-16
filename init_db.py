import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def execute_sql_file(conn, filepath):
    with open(filepath, 'r') as f:
        sql = f.read()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()

if __name__ == "__main__":
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise Exception("DATABASE_URL não definida no .env")
    
    conn = psycopg2.connect(dsn)
    try:
        print("Criando tabelas base...")
        execute_sql_file(conn, "src\queries\createTables.sql")
        print("Criando tabelas derivadas...")
        execute_sql_file(conn, "src\queries\createDerivedTables.sql")
        print("Tabelas criadas com sucesso!")
    finally:
        conn.close()