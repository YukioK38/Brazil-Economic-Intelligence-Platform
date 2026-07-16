import pandas as pd
import numpy as np

def clean_series(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset=['date'])
    df = df.sort_values('date')
    return(df)

def calc_yoy_variation(df: pd.DataFrame) -> pd.DataFrame:
    df = df.set_index("date").sort_index()
    df['value'] = df["value"].pct_change(periods=12)*100
    df['value'] = df['value'].replace([np.inf, -np.inf], np.nan)
    return(df.reset_index())

def calc_daily_variation(df: pd.DataFrame) -> pd.DataFrame:
    df = df.set_index("date").sort_index()
    df["value"] = df['value'].pct_change()*100
    df["value"] = df['value'].replace([np.inf, -np.inf], np.nan)
    return(df.reset_index())

