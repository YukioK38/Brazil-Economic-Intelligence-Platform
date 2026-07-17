import requests
import pandas as pd
from datetime import date, datetime

def get_bacen_series(code:int, start_date:str, end_date: str | None = None) -> pd.DataFrame:

    if end_date is None:
        end_date = date.today().strftime('%d/%m/%Y')

    # Bacen can return a bad gateway if too much data is requested, so we must split it into chunks (by year)
    start_dt = datetime.strptime(start_date, '%d/%m/%Y')
    end_dt = datetime.strptime(end_date, '%d/%m/%Y')

    all_chunks = []
    current_start = start_dt

    while current_start <= end_dt:
        # limits each run to one yeat
        current_end = min(current_start.replace(year=current_start.year + 1) - pd.Timedelta(days=1), end_dt)
        
        # gets a time series from BACEN, using the code and start/end dates. Returns a pandas dataframe
        url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados'
        param = {'formato': 'json'}
        param['dataInicial'] = current_start.strftime('%d/%m/%Y')
        param['dataFinal'] = current_end.strftime('%d/%m/%Y')

        resp = requests.get(url, params=param, timeout=60)
        resp.raise_for_status()
        all_chunks.append(pd.DataFrame(resp.json()))

        current_start = current_end + pd.Timedelta(days=1)

    df = pd.concat(all_chunks, ignore_index=True)
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    df = df.rename(columns={'data': 'date', 'valor':'value'})
    df['sgs_code'] = code
    df = df.drop_duplicates(subset=['date'], keep='last').sort_values('date').reset_index(drop=True)

    return(df)

# Usage example
if __name__ == '__main__':
    selic = get_bacen_series(432, start_date='01/01/2020', end_date='01/01/2025')
    print(selic.head())



