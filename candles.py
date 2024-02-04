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

    flat: False
    bullish: False
    bearish: False

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


class T2Candle:
    for_buyer: False
    for_seller: False
    uptake: False
    pushdown: False


class TLimits:
    body = False
    wick = False
    up = False
    dn = False
    close_open = False

    # to-do: list of candles for Limits ? or included from candle0 to candle1 ?
    candle0: TCandle
    candle1: TCandle

    def set_up(self, candle0, candle1: TCandle):
        self.candle0 = candle0
        self.candle1 = candle1
        self.wick = True
        self.up = True

    def set_dn(self, candle0, candle1: TCandle):
        self.candle0 = candle0
        self.candle1 = candle1
        self.wick = True
        self.dn = True

    def set_up_body(self, candle0, candle1: TCandle):
        self.candle0 = candle0
        self.candle1 = candle1
        self.body = True
        self.up = True

    def set_dn_body(self, candle0, candle1: TCandle):
        self.candle0 = candle0
        self.candle1 = candle1
        self.body = True
        self.dn = True


class TCandleData(DataFrame):
    pass


class TCandlesList(list):
    limits: TLimits

    def __init__(self):
        super().__init__()
        self.limits = TLimits()


class TCandlesData:
    week1: TCandleData
    day1: TCandleData
    hour1: TCandleData
    min5: TCandleData

    interval = {}  # other intervals and links to std-intervals


class TCandlesCollection:
    week1 = TCandlesList
    day1 = TCandlesList
    hour1 = TCandlesList
    min5 = TCandlesList

    interval = {}  # other intervals and links to std-intervals

    def __init__(self):
        self.day1 = TCandlesList()



