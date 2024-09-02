from drawer import *
from symbols import *


class AnalysisRule:  # ?
    pass


class AnalysisRules:  # ? for Methods????
    pass


class AnalysisMethod:
    # symbol: Symbol
    candles: TCandlesList = None
    drawer: TDrawer
    ax = None
    visible = False

    def __init__(self, s: Symbol, candles: TCandlesList, _ax, visible=True):
        self.symbol = s
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

    def skip_i(self):
        c = self.candles
        i = 0
        while i < len(c) and c[i].dt < c.dtcalc[0]:  # пропустить, до свечи, с которой начать расчет
            i += 1
        return i


class AnalysisSystem:
    metas: MetaSymbols
    methods = []
    drawer: TDrawer = None

    def __init__(self, drawer: TDrawer):
        # self.meta = m
        self.drawer = drawer

    def main(self):
        for m in self.methods:
            m.calc()

    def draw(self):
        if self.drawer is not None:
            for m in self.methods:
                m.drawer = self.drawer
                if m.visible: m.draw()

            self.drawer.show()

    async def amain(self):
        pass


class TBaseSystem:
    pass


class TMetaSystem:
    pass


class TFractalSystem:
    pass
