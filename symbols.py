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
    # from_1d: datetime
    # to_1d: datetime
    ignore_candles_count: int

# @dataclass(eq=False, repr=True)
# class DTFromToInfo:
#     dtfrom: dict[datetime]


class Symbol:
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

    dtfrom: {Interval}
    dtto: {Interval}

    def get_title(self):
        if self.info.is_future:
            return 'FUTURE: ' + self.ticker + '/' + self.figi
        if self.info.is_spot:
            return 'SPOT: ' + self.ticker + '/' + self.figi
        else:
            return self.ticker

    def __init__(self, name, ticker, figi, connector: TConnector, **kwargs):
        self.info = SymbolInfo(
            first_1min_candle_date=datetime(1979, 7, 28),
            first_1day_candle_date=datetime(1979, 7, 28),
            extra='',
            is_future=False,
            is_spot=False,
            # from_1d=datetime(1979, 7, 28),
            # to_1d=datetime(1979, 7, 28),
            ignore_candles_count=0
        )

        self.dtfrom = dict()
        self.dtto = dict()

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

    def get(self, interval: Interval):
        if interval == Interval.day1:
            return self.data.day1
        elif interval == Interval.week1:
            return self.data.week1

    # def get_from(self, interval: Interval):
    #     if interval == Interval.day1:
    #         # return self.info.from_1d
    #         return self.get(interval).dtfrom
    #
    # def get_to(self, interval: Interval):
    #     if interval == Interval.day1:
    #         # return self.info.to_1d
    #         return self.get(interval).dtto

    def get_candles(self, interval: Interval):
        print('=======', interval)
        c = self.candles.get(interval)
        data = self.connector.get_candles(self.figi, interval, c.dtfrom, c.dtto)

        # self.get(interval) = data

        if interval == Interval.day1:
            self.data.day1 = data
        elif interval == Interval.week1:
            self.data.week1 = data

        self.refresh(interval)
        return self.candles.get(interval)

        # self.oi.data_oi.day1 = self.oi.connector.get_oi(self.oi.name)  # oi 5 min !!!! not 1 day!!!
        # todo пернести OI

    def refresh_inside(self, candles_list: TCandlesList, candles_df: TCandlesDataFrame):
        candles_list.clear()
        i = 0
        while i < candles_df.shape[0]:
            d = candles_df.iloc[i]
            c = TCandle(d['ts'], d['dt'], d['open'], d['high'], d['low'], d['close'], d['volume'], True)
            candles_list.append(c)
            i = i + 1
        self.candles.max_all_high = candles_df['high'].max()
        self.candles.min_all_low = candles_df['low'].min()

    def refresh(self, interval, ignore_candles_count=0):  # interval=Interval.all - по умолчанию: обновить все интервалы
        # todo и обновлять открытый интерес --- вообще обновлять всю дату, которая есть
        print('refresh_____', interval)
        if interval == Interval.day1:
            self.refresh_inside(self.candles.day1, self.data.day1)
        elif interval == Interval.week1:
            self.refresh_inside(self.candles.week1, self.data.week1)

        self.info.ignore_candles_count = ignore_candles_count


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

    def get_from(self, interval: Interval):  # тоже надо анализировать если нет записи в конфиге
        return self._from(self.cfg('from.'+Interval.cfgt(interval)))

    def get_to(self, interval: Interval):
        if self.cfg_has('to.' + Interval.cfgt(interval)):
            return self._from(self.cfg('to.' + Interval.cfgt(interval)))
        else:
            return now()

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

    def add_interval(self, s: Symbol, i: Interval):  # todo ---> Symbol
        c = s.candles.get(i)
        c.dtfrom = self.get_from(i)
        c.dtto = self.get_to(i)

    def add_spot(self, name: str):
        if self.cfg_has(name):
            conn = self.connectors.find_connector(self.cfg1(name))
            spot = conn.get_spot(self.cfg2(name))[0]  # пока первый найденный [0]
            print(name, ':', spot.ticker, spot.figi)

            s = self.symbols.append(Symbol(spot.name, spot.ticker, spot.figi, conn, spot=True))
            s.quoted = True

            # пока так, потом искать в конфиге
            self.add_interval(s, Interval.day1)
            self.add_interval(s, Interval.week1)

            return s

    def add_futures(self, name: str):
        if self.cfg_has(name):
            conn = self.connectors.find_connector(self.cfg1(name))

            if self.cfg2(name) == '*':  # search
                futures = conn.get_futures(self.alias)
                if futures is None:
                    print('no one futures for', self.alias)
                else:
                    for future in futures:
                        fut_s = self.symbols.append(
                            Symbol(future.name, future.ticker, future.figi, conn, future=True))
                        print(fut_s.ticker)
                    # current future
                    f = self.find_by_ticker(futures[0].ticker)
                    f.quoted = True

                    # пока так, потом искать в конфиге
                    self.add_interval(f, Interval.day1)
                    self.add_interval(f, Interval.week1)

                    print('current future = ' + f.ticker, f.figi)
                    return f
            else:
                # current future
                # self.future = self.cfg2('futures') -- это неправильно, пока только через поиск
                pass

    def add_open_interest(self, name: str):
        if self.cfg_has(name):
            conn = self.connectors.find_connector(self.cfg1('oi'))
            s = self.symbols.append(Symbol('', self.cfg2('oi'), '', conn))
            print('OI (open interest) = ' + s.name)
            return s

    # def add_interval(self, i: Interval):
    #     self.spotT0 = self.add_spot('spot.T0', i)
    #     self.spotT1 = self.add_spot('spot.T1', i)
    #     self.future = self.add_futures('futures', i)
    #     self.oi = self.add_open_interest('oi', i)

    def main(self):
        # не так, система должна добавлять интервалы, а здесь проверять что она добавила и добавлять

        # self.add_interval(Interval.day1)
        # self.add_interval(Interval.week1)

        self.spotT0 = self.add_spot('spot.T0')
        self.spotT1 = self.add_spot('spot.T1')
        self.future = self.add_futures('futures')
        self.oi = self.add_open_interest('oi')


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




        # @staticmethod
        # def MetaSymbol.sync(a, b: Symbol, interval: Interval):  # не используется -- 2графика в 1 окне не синхронизируются как нужно
        #     da = a.get(interval)
        #     db = b.get(interval)
        #     delta = len(da) - len(db)
        #     print('delta', delta)
        #     low = db.iloc[0]['low']
        #
        #     if delta > 0:  # если у фуча меньше свечей, то:
        #         dd = da.head(delta-1)
        #         dd['open'] = low
        #         dd['close'] = low
        #         dd['low'] = low
        #         dd['high'] = low
        #         dd['volume'] = 0
        #
        #         if interval == Interval.day1:
        #             b.data.day1 = pd.concat([dd, db])
        #             b.data.day1.reindex()  # todo need?
        #             print(da.head(8))
        #             print(db.head(8))
        #             print(dd)
        #             print(b.data.day1.head(8))
        #
        #         b.refresh(delta)