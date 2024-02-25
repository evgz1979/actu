from connector import *
from drawer import *
from trader import *
from orm import *
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
import configparser

from system import TAnalysisSystem
from symbols import *


class TDataFeeder:
    pass


class TRobot:
    data: TDataFeeder
    config: configparser.ConfigParser
    connectors = []
    symbols = []
    meta_symbols = []
    # system: TAnalysisSystem = None
    # drawer: TDrawer = None

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

    def main(self):  #, system, drawer):
        # self.system = system
        #self.drawer = drawer

        logger.info("connectors starting ...")

        # for key, connector in self.connectors.items():
        for connector in self.connectors:
            connector.main()

        logger.info("meta symbols init ...")
        for ms in self.meta_symbols:
            logger.info("... meta symbol: " + ms.alias + ' ...')

            s1 = None

            spots = ms.connector.get_spot('USD000UTSTOM')
            # spots = ms.connector.get_currency()
            # print('spot num', len(spots))
            #
            # for spot in spots:
            #     print(spot.name, spot.ticker, spot.figi)

            for spot in spots:
                # print('spot: ' + spot.name)
                s = TSymbol(spot.name, spot.ticker, spot.figi, ms.connector, spot=True)
                if s1 is None:
                    s1 = s
                    s.quoted = True
                    s.first_1min_candle_date = spot.first_1min_candle_date
                    s.first_1day_candle_date = spot.first_1day_candle_date
                    ms.spot_T1 = s
                    print('spot_T1 (TOM, tomorow) = ' + ms.spot_T1.ticker)

                ms.symbols.append(s)

            # isin: str = _grpc_helpers.string_field(1)
            # figi: str = _grpc_helpers.string_field(2)
            # ticker: str = _grpc_helpers.string_field(3)
            # class_code: str = _grpc_helpers.string_field(4)
            # instrument_type: str = _grpc_helpers.string_field(5)
            # name: str = _grpc_helpers.string_field(6)
            # uid: str = _grpc_helpers.string_field(7)
            # position_uid: str = _grpc_helpers.string_field(8)
            # instrument_kind: "InstrumentType" = _grpc_helpers.enum_field(10)
            # api_trade_available_flag: str = _grpc_helpers.string_field(11)
            # for_iis_flag: bool = _grpc_helpers.bool_field(12)
            # first_1min_candle_date: datetime = _grpc_helpers.message_field(26)
            # first_1day_candle_date: datetime = _grpc_helpers.message_field(27)
            # for_qual_investor_flag: bool = _grpc_helpers.bool_field(28)
            # weekend_flag: bool = _grpc_helpers.bool_field(29)
            # blocked_tca_flag: bool = _grpc_helpers.bool_field(30)


            # spots = ms.connector.get_spot(self.config.get('META: USD/RUB', 'spot_T0'))
            # s_t1 = TSymbol(spots[0].name, spots[0].ticker, spots[0].figi, ms.connector, spot=True)
            # s_t1.quoted = True
            # ms.spot_T0 = s_t1
            # logger.info('spot_T0 = (TOD, today) = ' + ms.spot_T0.ticker)

            futures = ms.connector.get_futures(ms.alias)
            for future in futures:
                ms.symbols.append(TSymbol(future.name, future.ticker, future.figi, ms.connector, future=True))
            if len(futures) > 0:
                ms.future_current = futures[0]
                ms.future_current.quoted = True
                print('current future = ' + ms.future_current.ticker)

            ms.main()

        # if self.system: self.system.main()

        # logger.info("starting async data.amain() ...")
        # self.amain()

    def amain(self):  # data.amain() is not async !!! - async only connector.amain() and system.amain()

        # if self.system: self.system.amain()

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
