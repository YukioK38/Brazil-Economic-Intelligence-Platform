from src.transformations import clean_series
from src.db_functions import fetch_indicator_values, upsert_derived_indicator, insert_derived_values

def run_etl(con, base_indicator_id, name_suffix, calc_func, formula_desc):
    with con.cursor() as cur:
        raw = fetch_indicator_values(cur, base_indicator_id)
        raw = clean_series(raw)
        derived = calc_func(raw)

        derived_id = upsert_derived_indicator(cur, name_suffix, base_indicator_id, formula_desc)
        insert_derived_values(cur, derived_id, derived)
    con.commit()
