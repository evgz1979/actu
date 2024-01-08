from connector import *
from orm import *
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
import configparser


class TCandles(List):
    day1: DataFrame
    hour1: DataFrame
    min5: DataFrame


class TSymbol:
    name = ''
    ticker = ''
    figi = ''

    quoted = False
    is_future = False
    is_spot = False

    connector: TConnector
    _orm_symbol: Symbol
    _orm_candle: Candle

    candles: TCandles  # so far so

    def __init__(self, name, ticker, figi, connector, **kwargs):
        self.name = name
        self.ticker = ticker
        self.figi = figi
        self.connector = connector
        self.is_future = kwargs.get('future', False)
        self.is_spot = kwargs.get('spot', False)
        self.quoted = kwargs.get('quoted', False)

        self.candles = TCandles()


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
    config: configparser.ConfigParser

    def __init__(self, alias, connector, config):
        self.connector = connector
        self.config = config

        self.alias = alias
        self.name = config.get('META: ' + alias, 'name')

    def main(self):
        for symbol in self.symbols:
            logger.info(f"name={symbol.name}, ticker={symbol.ticker}, figi={symbol.figi}, quoted={symbol.quoted}")

        # self.current_spot.candles_day1 = \
        #     self.current_spot.connector.get_candles(self.current_spot.figi, Interval.day1)
        # print(self.current_spot.candles_day1)

        # print(self.config.get('META: '+self.alias, 'from_day'))

        nn = now()
        from22 = datetime.strptime(self.config.get('META: ' + self.alias, 'from_day'), '%Y-%m-%d').astimezone(nn.tzinfo)
        print(from22)

        self.current_spot.candles.day1 = \
            self.current_spot.connector.get_candles(
                self.current_spot.figi, Interval.day1, from22, now())

        print(self.current_spot.candles.day1)

        # symbol.candles[Interval.day1] = symbol.connector.get_candles(symbol.figi, Interval.day1)
        # df = symbol.connector.get_candles(symbol.figi, Interval.day1)
        # print(df)
        # symbol.candles[Interval.hour1] = symbol.connector.get_candles(symbol.name, Interval.hour1)


class TDataFeeder:
    config: configparser.ConfigParser
    connectors = []
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

        self.config = configparser.ConfigParser()
        self.config.read('cfg/settings.ini')

    def main(self):
        logger.info("connectors starting ...")

        # for key, connector in self.connectors.items():
        for connector in self.connectors:
            connector.main()

        logger.info("meta symbols init ...")
        for ms in self.meta_symbols:
            logger.info("... meta symbol: " + ms.alias + ' ...')

            futures = ms.connector.get_futures(ms.alias)
            for future in futures:
                ms.symbols.append(TSymbol(future.name, future.ticker, future.figi, ms.connector, future=True))
            if len(futures) > 0:
                ms.current_future = ms.symbols[0]  # futures[0]
                ms.current_future.quoted = True
                logger.info('current future = ' + ms.current_future.ticker)

            s1 = None
            spots = ms.connector.get_spot(ms.name)
            for spot in spots:
                s = TSymbol(spot.name, spot.ticker, spot.figi, ms.connector, spot=True)
                if s1 is None:
                    s1 = s
                    s.quoted = True
                    ms.current_spot = s
                    logger.info('current spot = ' + ms.current_spot.ticker)

                ms.symbols.append(s)

            ms.main()

        logger.info("starting async data.amain() ...")
        self.amain()

    def amain(self):  # data.amain() is not async !!! - async only connector.amain()
        for connector in self.connectors:
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

    # config = configparser.ConfigParser()  # -> data
    #
    # config.add_section('CONNECTOR: TINKOFF')
    # config.set('CONNECTOR: TINKOFF', 'token',
    #            '')
    # config.set('CONNECTOR: TINKOFF', 'app_name',
    #            'ACTUaliZator 0.1 by JZ')
    #
    # with open('cfg/settings.ini', 'w') as config_file:
    #     config.write(config_file)
    #
    # config.read('cfg/settings.ini')
    # print(config.get('SYMBOLS', 'meta_symbols')
