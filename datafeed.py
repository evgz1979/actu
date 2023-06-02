from typing import List, Union, Any

import pandas as pd
from sqlalchemy.engine import ScalarResult

from connector import *
from orm import *
from datetime import datetime

quoted_symbols = []

def get_candles(symbol_name: str, interval: str, dt_from: datetime, dt_to: datetime):
    print('>> get_candles(', symbol_name, ', ', interval, 'dt:', dt_from, ' -> ', dt_to, ')')


def candles_to_df3(candles):  # temp function
    df = pd.DataFrame(candles, columns='ts open high low close volume'.split()).astype(
        {'ts': int, 'open': float, 'high': float, 'low': float, 'close': float, 'volume': float})
    df.insert(1, 'dt', '')
    df['dt'] = df.apply(lambda x: timestamp2iso(x['ts'], format='%Y-%m-%d %H:%M:%S'), axis=1)
    df.insert(1, 'interval', 1)
    return df.set_index('ts')


def get_candles_old(s: str, interval):
    a = kus.fetch_ohlcv(s, interval, limit=500)
    return a


def get_quoted_symbols():
    with Session(engine) as session:
        statement = select(Symbol).where(Symbol.quoted)
        results = session.exec(statement)
        for symbol in results:
            quoted_symbols.append(symbol)


# symbol1 = Symbol(name='BTC/USDT', exchange_name='kucoin', exchange_section='futures',
#                  dt_analyzer_start_from=datetime.now(), dt_historical_start=datetime.now(),
#                  quoted=True)
# session.add(symbol1)
# session.commit()

print('>> datafeed init')
get_quoted_symbols()



# ----
# --- это реализация с другой проги df = pd.DataFrame(r.json()['data']).astype({'timestamp':int, 'open':float, 'close':float, 'high':float, 'low':float}).set_index('timestamp')
