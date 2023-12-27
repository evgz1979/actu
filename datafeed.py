from connector import *
from orm import *
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class TCandle:
    _orm: Candle


class TInterval:
    name: str
    candles: List[TCandle]

    def __init__(self, name):
        self.name = name


class TSymbol:
    name = ''
    figi = ''

    _connector_name: ''
    _orm: Symbol
    _related: ['TSymbol']

    intervals = {}

    def __init__(self, name, connector_name):
        self.name = name
        self.figi = name
        self._connector_name = connector_name


class TDataFeeder:
    connectors = {}
    symbols = [TSymbol]
    #  db = TDataBase
    quoted_by_orm = []
    _quoted_symbol_0 = Symbol

    def _print_0(self):  # temp
        for qs11 in self.quoted_by_orm:
            print('   * quoted symbol: ',
                  qs11.name)  # ,'... please wait while quoted symbol refreshing candles data ...')
            # refresh_quoted_symbol(qs)

    def _load_from_db(self):
        with Session(engine) as session:
            statement = select(Symbol).where(Symbol.quoted)

            results = session.exec(statement)

            for symbol in results:  ### упростить и объеденить нижний блок такойжке
                self.quoted_by_orm.append(symbol)

            if len(self.quoted_by_orm) == 0:
                print('adding quoted_symbol_0')
                session.add(self._quoted_symbol_0)
                session.commit()

                results = session.exec(statement)

                for symbol in results:
                    self.quoted_by_orm.append(symbol)

    def __init__(self):
        # temp - quoted_symbol_0 - если нет котируемых символов нигде в базе, пока временно используем этот,
        # позже сделать чтобы спрашивал из возможных вариантов
        self._quoted_symbol_0 = Symbol(name='BTC/USDT', exchange_name='kucoin', exchange_section='spot',
                                      dt_analyzer_start_from=datetime.now(), dt_historical_start=datetime.now(),
                                      quoted=True)
        self._load_from_db()

    def main(self):
        for key, connector in self.connectors.items():
            connector.main()

        for symbol in self.symbols:
            symbol.intervals['d1'] = TInterval('d1')
            symbol.intervals['h1'] = TInterval('h1')
            symbol.intervals['m5'] = TInterval('m5')

    def amain(self):  # data.amain() is not async !!! - async only connector.amain()
        for key, connector in self.connectors.items():
            asyncio.run(connector.amain())

    def get_candles(self, symbol: TSymbol, intervals):  # -> TIntervals
        pass


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



