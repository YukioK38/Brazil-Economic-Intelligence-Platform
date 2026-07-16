from src.data_collection import get_bacen_series
from src.db_functions import get_connection, upsert_indicator, insert_values
from src.pipeline import run_etl
from src.transformations import calc_daily_variation, calc_yoy_variation
from src.ibge_collection import get_sidra_series

BACEN_SERIES_CONFIG = {
    432:   {"name": "SELIC Meta",        "source": "BACEN", "frequency": "daily",   "unit": "%",     "transform":calc_daily_variation},
    433:   {"name": "IPCA",              "source": "BACEN", "frequency": "monthly", "unit": "%",     "transform":calc_yoy_variation},
    13522: {"name": "IPCA Acumulado 12m","source": "BACEN", "frequency": "monthly", "unit": "%",     "transform":None},
    188:   {"name": "INPC",              "source": "BACEN", "frequency": "monthly", "unit": "%",     "transform":calc_yoy_variation},
    189:   {"name": "IGP-M",             "source": "BACEN", "frequency": "monthly", "unit": "%",     "transform":calc_yoy_variation},
    24364: {"name": "IBC-Br",            "source": "BACEN", "frequency": "monthly", "unit": "index", "transform":None},
    1:     {"name": "Câmbio USD/BRL",    "source": "BACEN", "frequency": "daily",   "unit": "R$",    "transform": calc_daily_variation}
}

# Cada entrada do IBGE carrega os parâmetros necessários para montar a
# consulta SIDRA (tabela, variável, classificação/categoria opcionais).
IBGE_SERIES_CONFIG = {
    "IBGE_1620_583_90707": {
        "name": "PIB Trimestral (índice de volume)",
        "source": "IBGE",
        "frequency": "quarterly",
        "unit": "index (1995=100)",
        "table": 1620,
        "variable": 583,
        "classification": "c11255",
        "category": "90707",
    },
}

def ingest_bacen_Series(con, start_date:str, end_date:str | None = None) -> None:
    for code, meta in BACEN_SERIES_CONFIG.items():
        df = get_bacen_series(code, start_date="01/01/2020")
        with con.cursor() as cur:
            ind_id = upsert_indicator(
                cur, str(code), meta["name"], meta["source"], meta["frequency"], meta["unit"]
            )
            insert_values(cur, ind_id, df)
        con.commit()
    
        transform_func = meta.get("transform")
        if transform_func is not None:
            # removes calc_ from the function name to insert in the etl
            suffix = transform_func.__name__.replace("calc_", "")

            run_etl(con, ind_id, f"{meta["name"]}_{suffix}", transform_func, 
                    f"{suffix.replace("_", ' ').title()} of {meta['name']}")

def ingest_ibge_series(con) -> None:
    for code, meta in IBGE_SERIES_CONFIG.items():
        df = get_sidra_series(
            table=meta["table"],
            variable=meta["variable"],
            classification=meta.get("classification"),
            category=meta.get("category")
        )

        with con.cursor() as cur:
            ind_id = upsert_indicator(
                cur, code, meta["name"], meta["source"], meta["frequency"], meta["unit"]
            )
            insert_values(cur, ind_id, df)
        con.commit()


def main() -> None:
    con = get_connection()

    # Ingestion
    try:
        ingest_bacen_Series(con, start_date="01/01/2020", end_date=None)
        ingest_ibge_series(con)
    finally:
        con.close()

if __name__ == "__main__":
    main()