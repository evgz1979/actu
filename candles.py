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

    def __init__(self, candle0, candle1: TCandle, up=False, dn=False, gap=False, maker=False):
        self.candle0 = candle0
        self.candle1 = candle1

        self.up = up
        self.dn = dn
        self.gap = gap
        self.maker = maker


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


class TCandlesList(list[TCandle]):
    limits: TLimits
    moneys: TMoneys
    max_all_high: float
    min_all_low: float

    def __init__(self):
        super().__init__()
        self.limits = TLimits()
        self.moneys = TMoneys()


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



