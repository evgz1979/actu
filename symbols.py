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
    from_1d: datetime


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
            is_spot=False,
            from_1d=datetime(1979, 7, 28)
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

        # self.info.extra = self.connector.get_info(ticker)

    def get_from(self, interval: Interval):
        if interval == Interval.day1:
            return self.info.from_1d

    def get_candles(self, interval: Interval):
        data = self.connector.get_candles(self.figi, interval, self.get_from(interval), now())

        if interval == Interval.day1: self.data.day1 = data
        elif interval == Interval.week1: self.data.week1 = data

        self.refresh()
        return self.candles.get(interval)

        # self.oi.data_oi.day1 = self.oi.connector.get_oi(self.oi.name)  # oi 5 min !!!! not 1 day!!!
        # todo пернести OI

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


class Symbols(list[Symbol]):

    def append(self, __object: Symbol) -> Symbol:
        super().append(__object)
        return __object


class MetaSymbol:
    connectors: TConnectors = None

    name = ''
    alias = ''

    symbols: Symbols

    spotT0: Symbol = None
    spotT1: Symbol = None
    future: Symbol = None  # current future
    oi: Symbol = None

    related: [Symbols]  # todo -- это коррелирующие и др связанные инструменты

    # future_infinity: TSymbol = None
    # sT2: TSymbol = None

    def cfg(self, option):
        return config.get('META: ' + self.alias, option)

    def cfg_has(self, option):
        return config.has_option('META: ' + self.alias, option)

    def cfg1(self, key):
        return self.cfg(key).split(':')[0]

    def cfg2(self, key):
        return self.cfg(key).split(':')[1]

    @staticmethod
    def _from(s):
        moscow = timezone(timedelta(hours=3), "Moscow")
        return datetime.strptime(s, '%Y-%m-%d').astimezone(datetime.now(moscow).tzinfo)

    def __init__(self, alias):
        self.alias = alias
        self.name = config.get('META: ' + alias, 'name')
        self.symbols = Symbols()

    def find_by_ticker(self, ticker):
        r = None
        for s in self.symbols:
            if s.ticker == ticker:
                r = s
                return r

    def main(self):

        # get meta info for symbols
        f1 = self._from(self.cfg('from.1d'))

        if self.cfg_has('spot.T0'):  # spot T0
            conn = self.connectors.find_connector(self.cfg1('spot.T0'))
            self.spotT0 = self.symbols.append(
                Symbol(self.cfg2('spot.T0'), self.cfg2('spot.T0'), self.cfg2('spot.T0'), conn, spot=True))
            self.spotT0.info.from_1d = f1
            print('spot_T0 (TOD, today) = ' + self.spotT0.ticker)

        if self.cfg_has('spot.T1'):  # spot T1
            conn = self.connectors.find_connector(self.cfg1('spot.T1'))
            spot = conn.get_spot(self.cfg2('spot.T1'))
            self.spotT1 = self.symbols.append(
                Symbol(spot.name, spot.ticker, spot.figi, conn, spot=True))
            print('spot_T1 (TOM, tomorow) = ' + self.spotT1.ticker)

        if self.cfg_has('futures'):  # futures
            conn = self.connectors.find_connector(self.cfg1('futures'))

            if self.cfg2('futures') == '*':  # search
                futures = conn.get_futures(self.alias)
                if futures is None:
                    print('no one futures for', self.alias)
                else:
                    for future in futures:
                        fut_s = self.symbols.append(Symbol(future.name, future.ticker, future.figi, conn, future=True))
                        print(fut_s.ticker)
                    # current future
                    self.future = self.find_by_ticker(futures[0].ticker)
            else:
                # current future
                self.future = self.cfg2('futures')

            self.future.quoted = True
            self.future.info.from_1d = f1
            print('current future = ' + self.future.ticker)

        if self.cfg_has('oi'):  # open interest
            conn = self.connectors.find_connector(self.cfg1('oi'))
            self.oi = self.symbols.append(Symbol('', self.cfg2('oi'), '', conn))
            print('OI (open interest) = ' + self.oi.name)


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
