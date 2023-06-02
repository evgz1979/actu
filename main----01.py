from datetime import datetime, date

import requests

from connector import *
from orm import *
import pandas as pd
import finplot as fplt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def plot1(df1):  # temp function
    fplt.candlestick_ochl(df1[['open', 'close', 'high', 'low']])
    fplt.show()


def candles_to_df3(candles):  # temp function
    df = pd.DataFrame(candles, columns='ts open high low close volume'.split()).astype(
        {'ts': int, 'open': float, 'high': float, 'low': float, 'close': float, 'volume': float})
    df.insert(1, 'dt', '')
    df['dt'] = df.apply(lambda x: timestamp2iso(x['ts'], format='%Y-%m-%d %H:%M:%S'), axis=1)
    temp_interval_as_int = 1  # позже нужна таблица интервалов и их названий
    df.insert(1, 'interval', 1)
    return df.set_index('ts')

# df = pd.DataFrame(r.json()['data']).astype({'timestamp':int, 'open':float, 'close':float, 'high':float, 'low':float}).set_index('timestamp')


def get_candles(symbol_name, interval):
    a = kus.fetch_ohlcv(symbol_name, interval, limit=500)
    return a


def log(a):
    print(a)


log('started')
engine = create_engine("sqlite:////Users/evgz/py/b3/db/01.db", echo=False)
engine.connect()
Base.metadata.create_all(engine)
session = Session(engine)

df = candles_to_df3(get_candles(symbol_name_ku, '1w'))  # -- так работает с базой
#print(df)
# print('max=', df['high'].max(), '; min=', df['low'].min())
#plot1(df) # унифицировать df для базы и графика
#df.to_sql('candles', con=engine, if_exists='append')  # потом удалить неуник значения

