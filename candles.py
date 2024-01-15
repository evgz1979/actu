from datetime import datetime


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

    bullish: False
    bearish: False

    for_buyer: False
    for_seller: False
    uptake: False
    pushdown: False

    def __init__(self, ts: int, dt: datetime, open: float, high: float, low: float, close: float, volume: float,
                 is_complete: bool):
        self.ts = ts
        self.dt = dt
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.is_complete = is_complete


class TLimits:
    body = False
    wick = False
    up = False
    down = False


class T2Candles:
    candle1: TCandle
    candle2: TCandle
    limits: TLimits
