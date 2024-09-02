from settings import *
from base.info import *


class StreamItem:
    up: bool = False
    index: int
    candle_index: int
    enter: (int, float)  # ts, value
    exit: (int, float)
    # extr: (int, float)
    stop: (int, float)
    # value: (int, float)

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
        return cUp if self.up else cDn

    @property
    def value(self):
        return self.enter[1]

    def __init__(self, enter, _exit, stop=(0, 0), visible=False, candle_index=0, index=0):
        self.index = index
        self.candle_index = candle_index
        self.enter = enter
        self.exit = _exit
        self.stop = stop
        self.up = self.enter[1] < self.exit[1]
        self.visible = visible

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

