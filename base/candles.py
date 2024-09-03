from pandas import DataFrame
from base.stream import *
from base.info import *
from base.flow import *


class TCandlesDataFrame(DataFrame):
    dtfrom: datetime
    dtto: datetime
    # pass


class TOIData(DataFrame):
    pass


class TCandlesList(list[TCandle]):
    limits: TLimits
    moneys: TMoneys
    stream: Stream
    stream0: Stream
    stream1: Stream
    stream2: Stream
    # flow: Flow
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
        # self.flow = Flow()
        self.tendency = Tendency(self.stream)
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

