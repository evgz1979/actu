from connector import *
from orm import *
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


quoted_symbols = []
quoted_symbol_0 = Symbol(name='BTC/USDT', exchange_name='kucoin', exchange_section='spot',
                         dt_analyzer_start_from=datetime.now(), dt_historical_start=datetime.now(), quoted=True)


def refresh(self):
    print('refresh method ___')
    print(self.name)
    with Session(engine) as session:
        statement = select(Symbol)

        results = session.exec(statement)
        for r in results:
            print(r)


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


# ----
# --- это реализация с другой проги df = pd.DataFrame(r.json()['data']).astype({'timestamp':int, 'open':float, 'close':float, 'high':float, 'low':float}).set_index('timestamp')
