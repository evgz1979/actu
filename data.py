import pandas as pd
from settings import *


def candles_to_df3(candles):  # temp function
    df = pd.DataFrame(candles, columns='ts open high low close volume'.split()).astype(
        {'ts': int, 'open': float, 'high': float, 'low': float, 'close': float, 'volume': float})
    df.insert(1, 'dt', '')
    df['dt'] = df.apply(lambda x: timestamp2iso(x['ts'], format='%Y-%m-%d %H:%M:%S'), axis=1)
    temp_interval_as_int = 1  # позже нужна таблица интервалов и их названий
    df.insert(1, 'interval', 1)
    return df.set_index('ts')

# --- это реализация с другой проги df = pd.DataFrame(r.json()['data']).astype({'timestamp':int, 'open':float, 'close':float, 'high':float, 'low':float}).set_index('timestamp')


def get_candles(s: str, interval):
    a = kus.fetch_ohlcv(s, interval, limit=500)
    return a
