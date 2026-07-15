import requests
import pandas as pd

def _period_to_date(period_code: str) -> pd.Timestamp:

    year = int(period_code[:4])
    suffix = int(period_code[4:6])

    if suffix <= 4:
        month = (suffix - 1) * 3 + 1
    else:
        month = suffix
    return pd.Timestamp(year=year, month=month, day=1)

def get_sidra_series(
        table: int, # SIDRA table code
        variable: int, # Variable code inside table
        territory_level: str = "n1", # n1 for Brazil
        territory_code: str = "all", # all or particular region
        period: str = "all",
        classification: str | None = None,
        category: str | None = None
) -> pd.DataFrame:
    url_parts = [
        "https://apisidra.ibge.gov.br/values",
        f"t/{table}",
        f"{territory_level}/{territory_code}",
        f"v/{variable}",
        f"p/{period}"
    ]

    if classification and category:
        url_parts.append(f"{classification}/{category}")
    
    url = "/".join(url_parts)

    resp = requests.get(url, timeout=60)
    resp.raise_for_status()

    data = resp.json()


    print("Tamanho da lista:", len(data))
    print("Primeiro elemento (deveria ser um dado, não o cabeçalho):", data[0])

    data = data[1:]  # remove cabeçalho
    df = pd.DataFrame(data)
    print("Primeira linha do DataFrame:")
    print(df.iloc[0])


    df = pd.DataFrame(data)

    df["date"] = df["D3C"].apply(_period_to_date)
    df["value"] = pd.to_numeric(df["V"], errors = "coerce")
    df["sidra_table"] = table

    return df[["date", "value", "sidra_table"]].sort_values("date").reset_index(drop=True)


if __name__ == "__main__":
    pib = get_sidra_series(
        table=1620,
        variable=583,
        classification="c11255",
        category="90707",
    )
    print(pib.head())
    print(pib.dtypes)