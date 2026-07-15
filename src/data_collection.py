import requests
import pandas as pd
from datetime import date

def get_bacen_series(code:int, start_date:str, end_date: str | None = None) -> pd.DataFrame:

    if end_date is None:
        end_date = date.today().strftime('%d/%m/%Y')
    # gets a time series from BACEN, using the code and start/end dates. Returns a pandas dataframe
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados'
    param = {'formato': 'json'}
    param['dataInicial'] = start_date
    param['dataFinal'] = end_date

    resp = requests.get(url, params=param, timeout=60)
    resp.raise_for_status()

    df = pd.DataFrame(resp.json())
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    df = df.rename(columns={'data': 'date', 'valor':'value'})
    df['sgs_code'] = code
    return(df)

# Usage example
if __name__ == '__main__':
    selic = get_bacen_series(432, start_date='01/01/2020', end_date='01/01/2025')
    print(selic.head())



