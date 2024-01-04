from connector import *
from orm import *
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


class TSymbol:
    name = ''
    ticker = ''
    figi = ''

    quoted = False
    future = False
    spot = False

    connector: TConnector
    _orm_symbol: Symbol
    _orm_candle: Candle

    candles = {}

    def __init__(self, name, ticker, figi, connector, **kwargs):
        self.name = name
        self.ticker = ticker
        self.figi = figi
        self.connector = connector
        self.future = kwargs.get('future', False)
        self.spot = kwargs.get('spot', False)


class TMetaSymbol:
    name = ''
    alias = ''
    # figi = ''
    # future = ''
    # description = ''

    symbols = []
    current_future: TSymbol
    current_spot: TSymbol

    connector: TConnector

    def __init__(self, name, alias, connector):
        self.name = name
        self.alias = alias
        self.connector = connector

    def main(self):
        # logger.info("getting candles ...")
        for symbol in self.symbols:
            print(f"name=[{symbol.name}], ticker=[{symbol.ticker}], figi=[{symbol.figi}], future={symbol.future}")

            # logger.info("... for symbol = " + symbol.name)
            if symbol.quoted:
                symbol.candles[Interval.day1] = symbol.connector.get_candles(symbol.name, Interval.day1)
            # symbol.candles[Interval.hour1] = symbol.connector.get_candles(symbol.name, Interval.hour1)


class TDataFeeder:
    connectors = {}
    symbols = []
    meta_symbols = []

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
        logger.info("connectors starting ...")
        for key, connector in self.connectors.items():
            connector.main()

        logger.info("meta symbols init ...")
        for ms in self.meta_symbols:
            logger.info("... meta symbol: " + ms.alias + ' ...')

            futures = ms.connector.get_futures(ms.alias)
            for future in futures:
                ms.symbols.append(TSymbol(future.name, future.ticker, future.figi, ms.connector, future=True))
            if len(futures) > 0:
                ms.current_future = futures[0]
                logger.info('current future = ' + ms.current_future.ticker)

            spots = ms.connector.get_spot(ms.name)
            for spot in spots:
                ms.symbols.append(TSymbol(spot.name, spot.ticker, spot.figi, ms.connector, spot=True))
            if len(spots) > 0:
                ms.current_spot = spots[0]
                logger.info('current spot = ' + ms.current_spot.ticker)

            ms.main()

        self.amain()

    def amain(self):  # data.amain() is not async !!! - async only connector.amain()
        for key, connector in self.connectors.items():
            asyncio.run(connector.amain())


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
