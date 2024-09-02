from datetime import datetime


class Interval:
    all = 0
    day1 = 1
    week1 = 2
    month1 = 3
    hour1 = 10
    hour4 = 14
    min5 = 100

    @staticmethod
    def get_title(interval):
        if interval == Interval.min5: return '5 min'
        if interval == Interval.hour1: return '1 hour'
        if interval == Interval.day1: return '1 day'
        if interval == Interval.week1: return '1 week'

    @staticmethod
    def cfgt(interval):  # config_title
        if interval == Interval.min5: return '5m'
        if interval == Interval.hour1: return '1h'
        if interval == Interval.day1: return '1d'
        if interval == Interval.week1: return '1w'


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

    # max: float
    # min: float

    flat: bool
    bullish: bool
    bearish: bool

    for_buyer: bool
    for_seller: bool
    uptake: bool
    pushdown: bool

    enter: (int, float)
    exit: (int, float)

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

        # self.max = max(high, low)
        # self.min = min(high, low)

        if self.bullish:
            self.enter = (ts, low)
            self.exit = (ts, high)
        else:
            self.enter = (ts, high)
            self.exit = (ts, low)

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
