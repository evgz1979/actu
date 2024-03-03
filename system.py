from drawer import *
from symbols import *


class TAnalysisMethod:
    ms: TMetaSymbol
    candles: TCandlesList = None
    drawer: TDrawer
    ax = None
    visible = False

    def __init__(self, ms: TMetaSymbol, candles: TCandlesList, _ax, visible=True):
        self.ms = ms
        self.candles = candles
        self.ax = _ax
        self.visible = visible

    def calc(self):
        pass

    def acalc(self):  # asinc
        pass

    def draw(self):  # только расчет, без анализа
        pass

    def analisis(self):  # test? analize? --- анализирование данных
        pass

    def ts_max(self, _ts_: float):
        if _ts_ > self.candles[-1].ts:
            return self.candles[-1].ts
        else:
            return _ts_

    def ts_delta(self):
        return self.candles[1].ts - self.candles[0].ts


class TAnalysisSystem:
    ms: TMetaSymbol
    methods = []
    drawer: TDrawer

    def __init__(self, ms: TMetaSymbol, drawer: TDrawer):
        self.ms = ms
        self.drawer = drawer

    def main(self):
        for m in self.methods:
            m.calc()

    def draw(self):
        for m in self.methods:
            m.drawer = self.drawer
            m.draw()

    async def amain(self):
        pass


class TBaseSystem:
    pass


class TMetaSystem:
    pass
