from connector_moex import *
from orm import *
from candles import *
from drawer import *


class TSymbol:
    info: json
    name = ''
    ticker = ''
    figi = ''

    first_1min_candle_date: datetime
    first_1day_candle_date: datetime

    quoted = False
    is_future = False
    is_spot = False

    connector: TConnector = None
    _orm_symbol: Symbol
    _orm_candle: Candle

    data: TCandlesCollectionData  # so far so
    data_oi: TOICollectionData
    candles: TCandlesCollection  # so far so

    def __init__(self, name, ticker, figi, **kwargs):
        self.name = name
        self.ticker = ticker
        self.figi = figi
        # self.connector = connector
        self.is_future = kwargs.get('future', False)
        self.is_spot = kwargs.get('spot', False)
        self.quoted = kwargs.get('quoted', False)

        self.data = TCandlesCollectionData()
        self.data_oi = TOICollectionData()
        self.candles = TCandlesCollection()

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

        # for hour1 interval
        self.candles.hour1.clear()
        i = 0
        while i < self.data.hour1.shape[0]:
            d = self.data.hour1.iloc[i]
            c = TCandle(d['ts'], d['dt'], d['open'], d['high'], d['low'], d['close'], d['volume'], True)
            self.candles.hour1.append(c)
            i = i + 1


class TMetaSymbol:
    name = ''
    alias = ''

    symbols = []

    spotT0: TSymbol = None
    spotT1: TSymbol = None
    future: TSymbol = None
    oi: TSymbol = None

    # future_infinity: TSymbol = None
    # sT2: TSymbol = None

    def cfg(self, option):
        return config.get('META: ' + self.alias, option)

    @staticmethod
    def _from(s):
        return datetime.strptime(s, '%Y-%m-%d').astimezone(now().tzinfo)

    def __init__(self, alias):
        self.alias = alias
        self.name = config.get('META: ' + alias, 'name')

    def find_by_ticker(self, ticker):
        r = None
        for s in self.symbols:
            if s.ticker == ticker:
                r = s
                return r

    def main(self):
        f1 = self._from(self.cfg('from,1d'))
        f2 = self._from('2024-01-01')
        self.spotT1.data.day1 = self.spotT1.connector.get_candles(self.spotT1.figi, Interval.day1, f1, now())
        self.spotT0.data.day1 = self.spotT1.connector.get_candles(self.spotT0.figi, Interval.day1, f1, now())
        self.future.data.day1 = self.future.connector.get_candles(self.future.figi, Interval.day1, f1, now())

        self.spotT1.data.hour1 = self.spotT1.connector.get_candles(self.spotT1.figi, Interval.hour1, f2, now())

        self.oi.data_oi.day1 = self.oi.connector.get_oi(self.oi.name)  # oi 5 min !!!! not 1 day!!!

