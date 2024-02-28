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

    def between(self, i, ii, ii1):

        return (self[ii].up and self[ii].value <= self[i].value <= self[ii1].value) or \
               (not self[ii].up and self[ii1].value <= self[i].value <= self[ii].value)

    def find_min(self, si, si1: TStreamItem):
        i = self.index(si)
        i1 = self.index(si1)
        r = si
        while i < i1:
            if self[i].value < r.value: r = self[i]
            i += 1
        return r

    def find_max(self, si, si1: TStreamItem):
        i = self.index(si)
        i1 = self.index(si1)
        r = si
        while i < i1:
            if self[i].value > r.value: r = self[i]
            i += 1
        return r

    # def get_delta_ts(self):
    #     return (self[1].ts - self[0].ts) / (self[1].index - self[0].index)


class TTendencyPoint:
    si: TStreamItem = None
    enlarge = False
    index: int = 0
    range: int = 0
    breakp: int = 0
    prev: 'TTendencyPoint'  # break point

    def __init__(self, stream_item: TStreamItem, index, _range=0, prev=None):
        self.si = stream_item
        self.enlarge = False
        self.index = index
        self.prev = prev
        self.range = _range

    def coord(self, delta=0, value=0):
        if value != 0:
            v = value
        else:
            v = self.si.value
        return self.si.ts + delta, v


class TTendency(list[TTendencyPoint]):
    # frsi: int = 0  # first result stream index
    # lrsi: int = 0  # last result stream index

    def enlarge(self, ep: TTendencyPoint, si: TStreamItem, bp):
        ep.enlarge = True
        # ep.index = 1
        p = TTendencyPoint(si, 2, prev=ep.prev)
        self.append(p)
        return p

    def start2p(self, si0, si1: TStreamItem):  # start 2 point
        p1 = TTendencyPoint(si0, 1)
        p1.enlarge = True
        self.append(p1)
        p2 = TTendencyPoint(si1, 2, prev=p1)
        self.append(p2)
        return p2

    def add2p(self, ep, si, si1: TStreamItem):  # add 2 point
        ind = 1 if ep.enlarge else ep.index
        self.append(TTendencyPoint(si, ind + 1))
        p2 = TTendencyPoint(si1, ind + 2)
        self.append(p2)
        return p2

    def begin(self, start=0):
        if start == 0: i = len(self) - 1
        else: i = start

        while i >= 0:
            if self[i].enlarge:
                return self[i]
                # break
            i -= 1

    def between_last2p(self, si: TStreamItem):
        p_1 = self[-1].si  # last
        p_2 = self[-2].si  # pre last
        # p_2 = self.begin().si   # self[-2].si  # pre last

        return (p_2.up and p_2.value <= si.value <= p_1.value) or \
               (not p_2.up and p_1.value <= si.value <= p_2.value)


class TCorrectionPoint:
    stream_item: TStreamItem = None
    # parent: 'TTendencyNode' = None
    # inside: 'TTendencyNode' = None

    def __init__(self, parent, stream_item: TStreamItem):
        # self.parent = parent
        self.stream_item = stream_item


class TCorrection(list[TCorrectionPoint]):

    inside: 'TCorrection'
    parent: 'TCorrection'

    def between(self, si: TStreamItem):
        # if len(self) > 1:

        return (self[-2].stream_item.up and
                self[-2].stream_item.value <= si.value <= self[-1].stream_item.value) or \
               (not self[-2].stream_item.up and self[-1].stream_item.value <= si.value <= self[-2].stream_item.value)


# class TMetaFlow()  todo ?


class TCandlesList(list[TCandle]):
    limits: TLimits
    moneys: TMoneys
    stream: TStream
    tendency: TTendency

    max_all_high: float
    min_all_low: float

    def __init__(self):
        super().__init__()
        self.limits = TLimits()
        self.moneys = TMoneys()
        self.stream = TStream()
        self.tendency = TTendency()

    # delta ts
    def get_dts(self):
        return self[1].ts - self[0].ts


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



