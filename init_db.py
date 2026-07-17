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
        raise Exception("DATABASE_URL NOT DEFINED ON .env")
    
    conn = psycopg2.connect(dsn)
    try:
        execute_sql_file(conn, os.path.join("src", "queries", "createTables.sql"))
        execute_sql_file(conn, os.path.join("src", "queries", "createDerivedTables.sql"))
        print('Tables created')
    finally:
        conn.close()