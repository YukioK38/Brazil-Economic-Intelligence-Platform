import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


def get_connection():
    load_dotenv()
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

def upsert_indicator(cur, external_code, name, source, frequency, unit):
    # insert data and returns index, if conflict, return the index
    # of the existing entry
    cur.execute("""
        INSERT INTO indicators (external_code, indicator_name, source, frequency, unit)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (external_code) DO NOTHING
        RETURNING indicator_id                
    """, (external_code, name, source, frequency, unit))
    result = cur.fetchone()
    # returns id if inserted
    if result:
        return(result[0])
    # else finds the id of the existing entry
    cur.execute("SELECT indicator_id FROM indicators WHERE external_code = %s", (external_code,))
    return(cur.fetchone()[0])

def insert_values(cur, indicator_id, df):

    rows = [(indicator_id, row.date, row.value) for row in df.itertuples()] # faster than a for loop with appends
    execute_values(cur, """
        INSERT INTO indicator_values (indicator_id, date, value)
        VALUES %s
        ON CONFLICT (indicator_id, date) DO UPDATE SET value = EXCLUDED.value
    """, rows)

def upsert_derived_indicator(cur, name, base_indicator_id, formula_desc):
    cur.execute("""
        INSERT INTO derived_indicators (name, base_indicator_id, formula_desc)
        VALUES (%s, %s, %s)
        ON CONFLICT (name, base_indicator_id) DO NOTHING
        RETURNING derived_id
    """, (name, base_indicator_id, formula_desc))
    result = cur.fetchone()
    if result:
        return result[0]
    cur.execute("SELECT derived_id FROM derived_indicators WHERE name = %s", (name,))
    return cur.fetchone()[0]

def insert_derived_values(cur, derived_id, df):
    rows = [(derived_id, row.date, row.value) for row in df.itertuples()]
    execute_values(cur, """
        INSERT INTO derived_values (derived_id, date, value)
        VALUES %s
        ON CONFLICT (derived_id, date) DO UPDATE SET value = EXCLUDED.value
    """, rows)

def fetch_indicator_values(cur, indicator_id):
    cur.execute("""
        SELECT date, value FROM indicator_values
        WHERE indicator_id = %s
        ORDER BY date
    """, (indicator_id, ))
    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=["date", "value"])
    df['value'] = df['value'].astype(float)
    return(df)

'''
# example with the selic series from data collection
with con:
    with con.cursor() as cur:
        ind_id = upsert_indicator(cur, 432, "SELIC Meta", "BACEN", "daily", "%")
        insert_values(cur, ind_id, selic)
con.close()
'''