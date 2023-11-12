from connector import *
from orm import *
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

quoted_symbol_00 = Symbol(name='BTC/USDT', exchange_name='kucoin', exchange_section='spot',
                          dt_analyzer_start_from=datetime.now(), dt_historical_start=datetime.now(), quoted=True)


class TDataFeeder:
    connectors = []
    #  db = TDataBase
    quoted = []
    quoted_symbol_0 = Symbol

    def __init__(self, qs0):
        self.quoted_symbol_0 = qs0
        pass

    def load_from_db(self):
        with Session(engine) as session:
            statement = select(Symbol).where(Symbol.quoted)

            results = session.exec(statement)

            for symbol in results:  ### упростить и объеденить нижний блок такойжке
                self.quoted.append(symbol)

            if len(self.quoted) == 0:
                print('adding quoted_symbol_0')
                session.add(self.quoted_symbol_0)
                session.commit()

                results = session.exec(statement)

                for symbol in results:
                    self.quoted.append(symbol)

    def print_0(self):  # temp
        for qs11 in self.quoted:
            print('   * quoted symbol: ',
                  qs11.name)  # ,'... please wait while quoted symbol refreshing candles data ...')
            # refresh_quoted_symbol(qs)


def load_from_file(file_name: str):  # temp function --- >>> TCandles
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
    df.insert(0, 'dn', 0)
    df.insert(0, 'up', 0)
    return df
