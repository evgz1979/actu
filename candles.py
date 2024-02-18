from datetime import datetime
from pandas import DataFrame


class Interval:
    day1 = 1
    week1 = 2
    month1 = 3
    hour1 = 10
    min5 = 100


class TCandle:
    ts: int
    dt: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    is_complete: bool

    body_max: float
    body_min: float

    flat: bool
    bullish: bool
    bearish: bool

    for_buyer: bool
    for_seller: bool
    uptake: bool
    pushdown: bool

    def __init__(self, ts: int, dt: datetime, _open: float, high: float, low: float, close: float, volume: float,
                 is_complete: bool):
        self.ts = ts
        self.dt = dt
        self.open = _open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.is_complete = is_complete

        self.body_max = max(_open, close)
        self.body_min = min(_open, close)

        self.flat = _open == close
        self.bullish = close > _open
        self.bearish = _open > close

        self.for_buyer = False
        self.for_seller = False
        self.uptake = False
        self.pushdown = False


class TMoney:
    candle0: TCandle
    candle1: TCandle

    up = False
    dn = False
    gap: False
    maker: False
    limit: False

    def __init__(self, candle0, candle1: TCandle, up=False, dn=False, gap=False, maker=False):
        self.candle0 = candle0
        self.candle1 = candle1

        self.up = up
        self.dn = dn
        self.gap = gap
        self.maker = maker

        self.limit = (up and (candle1.open - candle0.close == 0)) or \
                     (dn and (candle0.close - candle1.open == 0))


class TLimit:
    candle0: TCandle
    candle1: TCandle

    value: float
    body = False
    wick = False
    up = False
    dn = False
    co = False  # close_open

    def __init__(self, candle0, candle1: TCandle, value, body=False, wick=False, up=False, dn=False, co=False):
        self.candle0 = candle0
        self.candle1 = candle1
        self.value = value

        self.body = body
        self.wick = wick
        self.up = up
        self.dn = dn
        self.co = co


class TLimits(list[TLimit]):
    pass


class TMoneys(list[TMoney]):
    pass


class TCandlesData(DataFrame):
    pass


class TOIData(DataFrame):
    pass


class TStreamItem:
    up: bool = False

    ts: int = 0
    value: float = 0
    index: int = 0

    stop_index: int = 0
    stop_ts: int = 0
    stop_value: float = 0

    maxmin: float = 0

    def __init__(self,
                 ts: int, value: float, index, stop_ts, stop_value, stop_index, up=False, maxmin: float = 0):
        self.ts = ts
        self.value = value
        self.index = index

        self.stop_ts = stop_ts
        self.stop_value = stop_value
        self.stop_index = stop_index

        self.up = up
        self.maxmin = maxmin

    def is_stop(self, ci, ci1: TCandle):  # c[i], c[i+1]
        if self.up:
            return ci1.low < ci.low
        else:
            return ci1.high > ci.high

    def is_duble_stop(self, ci, ci1: TCandle):  # c[i], c[i+1]
        if self.up:
            return ci1.high > ci.high
        else:
            return ci1.low < ci.low


class TStream(list[TStreamItem]):
    def get_df(self):
        df = DataFrame(columns=['ts', 'value'])
        for st in self:
            df.loc[len(df.index)] = [st.ts, st.value]
        return df

    def get_df_stop(self):
        dfs = DataFrame(columns=['ts', 'value'])
        for st in self:
            dfs.loc[len(dfs.index)] = [st.stop_ts, st.stop_value]
        return dfs

    def get_stop_value(self, ci):
        if self[-1].up:
            return ci.low
        else:
            return ci.high

    def get_stop_value_invert(self, ci):
        if self[-1].up:
            return ci.high
        else:
            return ci.low


class TCandlesList(list[TCandle]):
    limits: TLimits
    moneys: TMoneys
    stream: TStream

    max_all_high: float
    min_all_low: float

    def __init__(self):
        super().__init__()
        self.limits = TLimits()
        self.moneys = TMoneys()
        self.stream = TStream()


class TOICollectionData:
    day1: TOIData
    min5: TOIData


class TCandlesCollectionData:
    week1: TCandlesData
    day1: TCandlesData
    hour1: TCandlesData
    min5: TCandlesData

    interval = {}  # other intervals and links to std-intervals


class TCandlesCollection:
    week1 = TCandlesList
    day1 = TCandlesList
    hour1 = TCandlesList
    min5 = TCandlesList

    interval = {}  # other intervals and links to std-intervals

    def __init__(self):
        self.day1 = TCandlesList()



