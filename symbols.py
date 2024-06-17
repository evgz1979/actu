from dataclasses import dataclass
from datetime import *

from connector_moex import *
from connector_tinkoff import TBankConnector
from orm import *
from candles import *
from drawer import *


@dataclass(eq=False, repr=True)
class SymbolInfo:  # todo -- совместить позже с ORM
    first_1min_candle_date: datetime
    first_1day_candle_date: datetime
    extra: json
    is_future: bool
    is_spot: bool


class Symbol:  # DO NOT REFACTOR to Symbol !!!
    info: SymbolInfo
    name = ''
    ticker = ''
    figi = ''
    quoted = False

    connector: TConnector = None
    _orm_symbol: ORMSymbol
    _orm_candle: Candle

    data: TCandlesCollectionData  # so far so
    data_oi: TOICollectionData
    candles: TCandlesCollection  # so far so

    def __init__(self, name, ticker, figi, connector: TConnector, **kwargs):
        self.info = SymbolInfo(
            first_1min_candle_date=datetime(1979, 7, 28),
            first_1day_candle_date=datetime(1979, 7, 28),
            extra='',
            is_future=False,
            is_spot=False
        )

        self.name = name
        self.ticker = ticker
        self.figi = figi
        self.connector = connector
        self.info.is_future = kwargs.get('future', False)
        self.info.is_spot = kwargs.get('spot', False)
        self.quoted = kwargs.get('quoted', False)

        self.info.first_1min_candle_date = kwargs.get('first_1min_candle_date', False)
        self.info.first_1day_candle_date = kwargs.get('first_1day_candle_date', False)

        self.data = TCandlesCollectionData()
        self.data_oi = TOICollectionData()
        self.candles = TCandlesCollection()

        self.info.extra = self.connector.get_info(ticker)

    def refresh(self):
        # todo и обновлять открытый интерес --- вообще обновлять всю дату, которая есть

        # for day1 interval
        self.candles.day1.clear()
        i = 0
        while i < self.data.day1.shape[0]:
            d = self.data.day1.iloc[i]
            c = TCandle(d['ts'], d['dt'], d['open'], d['high'], d['low'], d['close'], d['volume'], True)
            self.candles.day1.append(c)
            i = i + 1

        self.candles.max_all_high = self.data.day1['high'].max()
        self.candles.min_all_low = self.data.day1['low'].min()

        # # for hour1 interval
        # self.candles.hour1.clear()
        # i = 0
        # while i < self.data.hour1.shape[0]:
        #     d = self.data.hour1.iloc[i]
        #     c = TCandle(d['ts'], d['dt'], d['open'], d['high'], d['low'], d['close'], d['volume'], True)
        #     self.candles.hour1.append(c)
        #     i = i + 1
        #
        # # for hour4 interval
        # self.candles.hour4.clear()
        # i = 0
        # while i < self.data.hour4.shape[0]:
        #     d = self.data.hour4.iloc[i]
        #     c = TCandle(d['ts'], d['dt'], d['open'], d['high'], d['low'], d['close'], d['volume'], True)
        #     self.candles.hour4.append(c)
        #     i = i + 1


class TSymbols(list[Symbol]):

    def append(self, __object: Symbol) -> Symbol:
        super().append(__object)
        return __object


class MetaSymbol:
    connectors: TConnectors = None
    moex: MOEXConnector
    tbank: TBankConnector

    name = ''
    alias = ''

    symbols: TSymbols

    spotT0: Symbol = None
    spotT1: Symbol = None
    future: Symbol = None
    oi: Symbol = None

    # future_infinity: TSymbol = None
    # sT2: TSymbol = None

    def cfg(self, option):
        return config.get('META: ' + self.alias, option)

    def cfg_ticker(self, key):
        return self.cfg(key).split(':')[1]

    @staticmethod
    def _from(s):
        moscow = timezone(timedelta(hours=3), "Moscow")
        return datetime.strptime(s, '%Y-%m-%d').astimezone(datetime.now(moscow).tzinfo)

    def __init__(self, alias):
        self.alias = alias
        self.name = config.get('META: ' + alias, 'name')
        self.symbols = TSymbols()

    def find_by_ticker(self, ticker):
        r = None
        for s in self.symbols:
            if s.ticker == ticker:
                r = s
                return r

    def main(self):

        # todo --------- пока все для Si ------ унифицировать !!!!

        self.moex = self.connectors.find_connector('MOEX')
        self.tbank = self.connectors.find_connector('TINKOFF')

        # spot T0
        self.spotT0 = self.symbols.append(Symbol('', self.cfg_ticker('spot.T0'), '', self.moex, spot=True))
        print('spot_T0 (TOD, today) = ' + self.spotT0.ticker)

        # spot T1
        spot = self.tbank.get_spot(self.cfg_ticker('spot.T1'))
        self.spotT1 = self.symbols.append(
            Symbol(spot.name, spot.ticker, spot.figi, self.tbank, spot=True, quoted=True,
                   first_1min_candle_date=spot.first_1min_candle_date,
                   first_1day_candle_date=spot.first_1day_candle_date))
        print('spot_T1 (TOM, tomorow) = ' + self.spotT1.ticker)

        # futures
        futures = self.tbank.get_futures(self.alias)
        for future in futures:
            fut_s = self.symbols.append(Symbol(future.name, future.ticker, future.figi, self.tbank, future=True))
            print(fut_s.ticker)

        # current future
        self.future = self.find_by_ticker(futures[0].ticker)
        self.future.quoted = True
        print('current future = ' + self.future.ticker)

        # open interest
        self.oi = oi = self.symbols.append(Symbol('', self.cfg_ticker('oi'), '', self.moex))
        print('OI (open interest) = ' + self.oi.name)

        f1 = self._from(self.cfg('from,1d'))
        f2 = self._from('2024-01-01')

        # self.spotT0.data.day1 = self.spotT1.connector.get_candles(self.spotT0.figi, Interval.day1, f1, now())

        # self.spotT1.data.day1 = self.spotT1.connector.get_candles(self.spotT1.figi, Interval.day1, f1, now())
        # self.spotT1.data.hour4 = self.spotT1.connector.get_candles(self.spotT1.figi, Interval.hour4, f2, now())
        # self.spotT1.data.hour1 = self.spotT1.connector.get_candles(self.spotT1.figi, Interval.hour1, f2, now())
        #
        self.future.data.day1 = self.future.connector.get_candles(self.future.figi, Interval.day1, f1, now())

        # self.future.data.hour1 = self.future.connector.get_candles(self.future.figi, Interval.hour1, f2, now())
        # self.future.data.hour4 = self.future.connector.get_candles(self.future.figi, Interval.hour4, f2, now())
        #
        # self.oi.data_oi.day1 = self.oi.connector.get_oi(self.oi.name)  # oi 5 min !!!! not 1 day!!!


class TMetaSymbols(list[MetaSymbol]):
    connectors: TConnectors

    def __init__(self, _connectors: TConnectors):
        super().__init__()
        self.connectors = _connectors

    def append(self, _ms: MetaSymbol) -> MetaSymbol:
        super().append(_ms)
        _ms.connectors = self.connectors
        return _ms

    def main(self):
        for ms in self:
            ms.main()
