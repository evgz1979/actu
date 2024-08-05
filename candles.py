from dataclasses import dataclass
from datetime import datetime
from pandas import DataFrame
from settings import *


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


class TCandlesDataFrame(DataFrame):
    dtfrom: datetime
    dtto: datetime
    # pass


class TOIData(DataFrame):
    pass


class StreamItem:
    up: bool = False
    index: int
    enter: (int, float)  # ts, value
    exit: (int, float)
    # extr: (int, float)
    stop: (int, float)
    value: (int, float)

    visible: bool

    # ts: int = 0
    # value: float = 0
    # index: int = 0
    #
    # stop_index: int = 0
    # stop_ts: int = 0
    # stop_value: float = 0
    #
    # maxmin: float = 0

    @property
    def color(self):
        if self.up: return cUp
        else: return cDn

    def __init__(self, enter, _exit, stop=(0, 0), visible=False, index=0):
        self.index = index
        self.enter = enter
        self.exit = _exit
        self.stop = stop
        self.up = self.enter[1] < self.exit[1]
        self.visible = visible

    #
    # def __init__(self, ts: int, value: float, index, stop_ts, stop_value, stop_index, up=False, maxmin: float = 0):
    #     self.ts = ts
    #     self.value = value
    #     self.index = index
    #
    #     self.stop_ts = stop_ts
    #     self.stop_value = stop_value
    #     self.stop_index = stop_index
    #
    #     self.up = up
    #     self.maxmin = maxmin
    #
    #     self.enter = 0
    #     self.exit = 0

    # @staticmethod
    # def is_smothing(ci, ci1: TCandle):
    #     return ci.enter[1] <= ci.exit[1] <= ci1.enter[1] or ci1.enter[1] <= ci.exit[1] <= ci.enter[1]

    # @staticmethod
    # def is_correction(ci, ci1: TCandle):
        # return (ci.bullish and ci1.bullish and ci.enter[1] <= ci1.enter[1] <= ci1.exit[1] and ci1.exit[1] > ci.exit[1]) or (
        #         ci.bearish and ci1.bearish and ci.enter[1] >= ci1.enter[1] >= ci.exit[1] > ci1.exit[1])
        # return (ci.bullish and ci.enter[1] <= ci1.low <= ci.exit[1] < ci1.high) or (
        #         ci.bearish and ci.enter[1] >= ci1.high >= ci.exit[1] > ci1.low)

    def merge(self, c: TCandle):
        if self.up:
            if c.high > self.exit[1]:
                if c.bullish:
                    self.exit = c.exit
                    self.stop = c.enter
                else:
                    self.exit = c.enter
                    self.stop = c.exit
        else:
            if c.low < self.exit[1]:
                if c.bullish:
                    self.exit = c.enter
                    self.stop = c.exit
                else:
                    self.exit = c.exit
                    self.stop = c.enter

    def is_stop2(self, ci, ci1: TCandle):  # c[i], c[i+1]
        if self.up:
            return ci1.low < ci.low  # and not ci.flat
        else:
            return ci1.high > ci.high  # and not ci.flat

    def get_stop(self, c: TCandle):  # c[i], c[i+1]
        if self.up:
            return c.ts, c.low
        else:
            return c.ts, c.high

    def is_stop(self, c: TCandle):  # c[i], c[i+1]
        # todo ignore.flat-candle
        # if self.up:
        #     r = ci1.low < ci.low  # and not ci.flat
        #     # if r: self.stop = ci.ts, ci.low
        # else:
        #     r = ci1.high > ci.high  # and not ci.flat
        #     # if r: self.stop = ci.ts, ci.high
        #
        # return r
        # return ((self.up and ci1.exit < ci.enter) or (not self.up and ci1.exit > ci.enter)) and not ci.flat
        return (self.up and c.low < self.stop[1]) or (not self.up and c.high > self.stop[1])

    def move_exit(self, ci, ci1: TCandle):
        # if self.up and ci1.high and not self.is_stop2(ci, ci1) > self.exit[1]: self.exit = ci1.ts, ci1.high  # and not ci.bullish
        # if not self.up and ci1.low and not self.is_stop2(ci, ci1) < self.exit[1]: self.exit = ci1.ts, ci1.low  # and not ci.bearish

        if self.up:
            if ci1.high > self.exit[1] and not (self.is_stop2(ci, ci1) and ci1.bullish): self.exit = ci1.ts, ci1.high
            return ci1.ts, ci1.low
        else:
            if ci1.low < self.exit[1] and not (self.is_stop2(ci, ci1) and ci1.bearish): self.exit = ci1.ts, ci1.low
            return ci1.ts, ci1.high

        # if self.up and ci1.low > ci.low: self.exit = ci1.ts, ci1.high
        # if not self.up and ci1.high < ci.high: self.exit = ci1.ts, ci1.low

    def move_stop(self, c: TCandle):
        if self.up: self.stop = c.ts, c.low
        else: self.stop = c.ts, c.high

    def is_duble_stop(self, ci, ci1: TCandle):  # c[i], c[i+1]
        if self.up:
            return ci1.high > ci.high
        else:
            return ci1.low < ci.low

    def get_exit(self, c: TCandle):  # ПЕРЕНЕС в move_exit
        if self.up:
            return c.ts, c.low
        else:
            return c.ts, c.high


class Stream(list[StreamItem]):

    def get_exit(self, si: StreamItem, ci, ci1: TCandle):
        pass
        # if si.up:
        #     return c.ts, c.low
        # else:
        #     return c.ts, c.high

    def normalize(self):
        pass
        # i = 0
        # while i < len(self):
        #     pass

    def append(self, __object: StreamItem) -> StreamItem:
        super().append(__object)
        return __object

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

    def find_min(self, si, si1: StreamItem):
        i = self.index(si)
        i1 = self.index(si1)
        r = si
        while i < i1:
            if self[i].enter[1] < r.enter[1]: r = self[i]
            i += 1
        return r

    def find_max(self, si, si1: StreamItem):
        i = self.index(si)
        i1 = self.index(si1)
        r = si
        while i < i1:
            if self[i].enter[1] > r.enter[1]: r = self[i]
            i += 1
        return r

    def find(self, f):
        for si in self:
            if si.enter[0] == f[0] or si.exit[0] == f[0]: return si

    # def get_delta_ts(self):
    #     return (self[1].ts - self[0].ts) / (self[1].index - self[0].index)


class FlowPoint:
    si: StreamItem = None
    enlarge = False
    index: int = 0
    up: bool
    # range: int = 0
    # breakp: int = 0
    # prev: 'TTendencyPoint'  # break point

    def __init__(self, stream_item: StreamItem, index, _range=0, prev=None, enlarge=False, up=True):
        self.si = stream_item
        self.index = index
        self.prev = prev
        self.range = _range
        self.enlarge = enlarge
        self.up = up

    def coord(self, delta=0, value=0):
        if value != 0:
            v = value
        else:
            v = self.si.enter[1]
        return self.si.enter[0] + delta, v

    def title(self):
        return str(self.index)
        # return '' if self.index == 1 else str(self.index)


        # if p.enlarge:
        #     return str(p.index)  # + "'" + str(p.range) + ", 1'" + str(p.range + 1)
        # else:
        #     return str(p.index)  # + "'" + str(p.range)


class SimpleFlow(list[FlowPoint]):
    frsi: FlowPoint = None  # first result stream index
    enter: FlowPoint
    exit: FlowPoint
    index: int

    def __init__(self, range_index=1):
        super().__init__()
        self.index = range_index

    def append(self, __object: FlowPoint) -> FlowPoint:
        super().append(__object)
        return __object

    def start(self, si0, si1: StreamItem):  # start 2 point
        self.enter = self.append(FlowPoint(si0, 1))
        self.exit = self.append(FlowPoint(si1, 2))
        self.frsi = self.enter
        return self.exit

    def add1p(self, si: StreamItem, index=0):  # add 1 point
        self.exit = self.append(FlowPoint(si, index + 1))
        return self.exit

    def add2p(self, si0, si1: StreamItem, index=0):  # add 2 point
        self.frsi = self.append(FlowPoint(si0, index))
        self.exit = self.append(FlowPoint(si1, index + 1))
        return self.exit

    def between_last2p(self, si: StreamItem):
        p2 = self[-1]
        p1 = self[-2]
        if p1.up: return p2.si.enter[1] >= si.enter[1] >= p1.si.enter[1]
        else: return p2.si.enter[1] <= si.enter[1] <= p1.si.enter[1]


class FlowRanges(list[SimpleFlow]):

    def append(self, __object: SimpleFlow) -> SimpleFlow:
        super().append(__object)
        return __object


class Flow:
    _current_range_index: int = 0  # for debug
    ranges: FlowRanges

    @property
    def range(self):
        if self._current_range_index == 0: return self.ranges[-1]  # current range
        else: return self.ranges[self._current_range_index-1]  # for debug

    def __init__(self):
        self.ranges = FlowRanges()
        self.ranges.append(SimpleFlow())

    def union(self, ep: FlowPoint, si: StreamItem):
        p1 = self.range[0]  # begin
        self.ranges.append(SimpleFlow(self.range.index+1))
        self.range.start(p1.si, ep.si)
        return self.range.add1p(si, 1)


class Tendency(Flow):
    pass


class Correction(Tendency):
    pass


class Structured(Correction):
    pass


class Volumed(Structured):
    pass


    # def enlarge(self, ep: TTendencyPoint, si: TStreamItem):
    #
    #     print('in enlarge, ep=', ep.index, 'begin=', self.begin().index)
    #
    #     i = ep.index - 1
    #     while i > self.begin().index:
    #         print('del=', i)
    #         self.pop(i-1)
    #         i -= 1
    #
    #     ep.enlarge = True
    #     return self.append(TTendencyPoint(si, 3))

        # return self.append(TTendencyPoint(si, 2, enlarge=True))
        # return self.append(TTendencyPoint(si, 3))

    # def start2p(self, si0, si1: StreamItem):  # start 2 point
    #     self.append(TendencyPoint(si0, 1))
    #     return self.append(TendencyPoint(si1, 2))

# class TendencyRanges(list[SimpleTendency]):
#
#     def append(self, __object: SimpleTendency) -> SimpleTendency:
#         super().append(__object)
#         return __object
#
#
# # class TendencyTree:
# #     point: SimpleTendency
#
#
# class Tendency:
#     ranges: TendencyRanges
#     stream: Stream
#     points: SimpleTendency
#
#     def __init__(self, stream: Stream):
#         self.stream = stream
#         self.ranges = TendencyRanges()
#         self.points = SimpleTendency()
#
#     def current(self):
#         return self.ranges[-1]
#
#     def start(self, si0, si1: StreamItem, range_index=1):
#         self.ranges.append(SimpleTendency(range_index))
#         return self.current().start2p(si0, si1)
#
#     def union(self, ep: TendencyPoint, si: StreamItem):
#         ep.enlarge = True
#         self.start(self.current().begin().si, ep.si, range_index=self.current().range_index + 1)
#         return self.current().append(TendencyPoint(si, 3, up=not ep.up))


# class TCorrectionPoint(TTendencyPoint):
#     pass
#
#
# class TCorrection(list[TCorrectionPoint]):
#     def start2p(self, si0, si1: TStreamItem):  # start 2 point
#         p1 = TCorrectionPoint(si0, 1)
#         p1.enlarge = True
#         self.append(p1)
#         p2 = TCorrectionPoint(si1, 2, prev=p1)
#         self.append(p2)
#         return p2

# class TCorrectionPoint:
#     stream_item: TStreamItem = None
#     # parent: 'TTendencyNode' = None
#     # inside: 'TTendencyNode' = None
#
#     def __init__(self, parent, stream_item: TStreamItem):
#         # self.parent = parent
#         self.stream_item = stream_item
#
#
# class TCorrection(list[TCorrectionPoint]):
#
#     inside: 'TCorrection'
#     parent: 'TCorrection'
#
#     def between(self, si: TStreamItem):
#         # if len(self) > 1:
#
#         return (self[-2].stream_item.up and
#                 self[-2].stream_item.value <= si.value <= self[-1].stream_item.value) or \
#                (not self[-2].stream_item.up and self[-1].stream_item.value <= si.value <= self[-2].stream_item.value)


class TCandlesList(list[TCandle]):
    limits: TLimits
    moneys: TMoneys
    stream: Stream
    stream0: Stream
    stream1: Stream
    stream2: Stream
    flow: Flow
    tendency: Tendency
    # correction: TCorrection

    max_all_high: float
    min_all_low: float

    dtload: (datetime, datetime)  # (from, to)
    dtcalc: (datetime, datetime)  # (from, to)

    # dtfrom: datetime
    # dtto: datetime

    def __init__(self):
        super().__init__()
        self.limits = TLimits()
        self.moneys = TMoneys()
        self.stream = Stream()
        self.stream0 = Stream()
        self.stream1 = Stream()
        self.stream2 = Stream()
        self.flow = Flow()
        self.tendency = Tendency()
        # self.correction = TCorrection()

    def _calc_dts(self):
        r = self[1].ts - self[0].ts
        if len(self) > 5:
            i = 1
            while i <= 5:
                a = self[i+1].ts-self[i].ts
                if a < r: r = a
                i += 1
        return r

    def ts_max(self, _ts_: float):
        if _ts_ > self[-1].ts:
            return self[-1].ts
        else:
            return _ts_

    def dts(self, value, multiple):  # delta ts
        return self.ts_max(value[0] + self._calc_dts() * multiple), value[1]


class TOICollectionData:
    day1: TOIData
    min5: TOIData


class TCandlesCollectionData:
    week1: TCandlesDataFrame
    day1: TCandlesDataFrame
    hour1: TCandlesDataFrame
    hour4: TCandlesDataFrame
    min5: TCandlesDataFrame

    interval = {}  # other intervals and links to std-intervals

    def get(self, interval: Interval):
        if interval == Interval.min5: return self.min5
        if interval == Interval.hour1: return self.hour1
        if interval == Interval.day1: return self.day1
        if interval == Interval.week1: return self.week1


class TCandlesCollection:
    week1 = TCandlesList
    day1 = TCandlesList
    hour1 = TCandlesList
    min5 = TCandlesList

    interval = {}  # other intervals and links to std-intervals

    def __init__(self):
        self.day1 = TCandlesList()
        self.week1 = TCandlesList()
        self.hour1 = TCandlesList()
        self.hour4 = TCandlesList()
        self.min5 = TCandlesList()

    def get(self, interval: Interval):
        if interval == Interval.min5: return self.min5
        if interval == Interval.hour1: return self.hour1
        if interval == Interval.hour4: return self.hour4
        if interval == Interval.day1: return self.day1
        if interval == Interval.week1: return self.week1




