from connector import *
from orm import *
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


quoted_symbols = []
quoted_symbol_0 = Symbol(name='BTC/USDT', exchange_name='kucoin', exchange_section='spot',
                         dt_analyzer_start_from=datetime.now(), dt_historical_start=datetime.now(), quoted=True)


def load_file(file_name: str):  # temp function
    df = pd.read_csv(file_name,
                 dtype={'date': str, 'time': str,
                        'open': float, 'high': float, 'low': float, 'close': float,
                        'volume': float})
    df['dt'] = pd.to_datetime(df['date'] + df['time'])  # as DateTime
    df.drop('date', axis=1, inplace=True)
    df.drop('time', axis=1, inplace=True)
    df['dt'] = df['dt'].astype(str)  # as str
    df.insert(0, 'ts', 0)
    df['ts'] = df.apply(lambda x: iso2timestamp(x['dt'], format='%Y-%m-%d %H:%M:%S'), axis=1)
    df.drop('dt', axis=1, inplace=True)
    df['ts'] = df['ts'].astype(int)
    # df.set_index('ts')
    df = df.set_index('ts')
    return df


def refresh_quoted_symbol(qs1: Symbol):
    with Session(engine) as session:
        statement = select(Symbol).where(Symbol.name == qs1.name)
        results = session.exec(statement)
        q = results.one()
        print(q.candles)


def get_quoted_symbols():
    with Session(engine) as session:
        statement = select(Symbol).where(Symbol.quoted)

        results = session.exec(statement)
        for symbol in results:
            quoted_symbols.append(symbol)

        if len(quoted_symbols) == 0:
            session.add(quoted_symbol_0)
            session.commit()

            results = session.exec(statement)
            for symbol in results:
                quoted_symbols.append(symbol)


def get_candles(symbol_name: str, interval: str):  # , dt_from: datetime, dt_to: datetime):
    print('>> get_candles(', symbol_name, ', ', interval, ')')  # , 'dt:', dt_from, ' -> ', dt_to, ')')

    with Session(engine) as session:
        statement = select(Candle)
        results = session.exec(statement)
        if results.first() is None:
            print('no one candle')  # и нужно закачивать -- или провкерять что нужного количества нет то тоже обновлять через коннектор


print('>> datafeed init')
get_quoted_symbols()
print('quoted symbols:')
for qs in quoted_symbols:
    print('*', qs.name, '... please wait while quoted symbol refreshing candles data ...')
    refresh_quoted_symbol(qs)



# ----
# --- это реализация с другой проги df = pd.DataFrame(r.json()['data']).astype({'timestamp':int, 'open':float, 'close':float, 'high':float, 'low':float}).set_index('timestamp')
