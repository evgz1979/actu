from drawer import TDrawer
from symbols import *


class TAnalysisMethod:
    ms: TMetaSymbol
    candles: TCandlesList = None
    drawer: TDrawer

    def __init__(self, ms: TMetaSymbol):
        self.ms = ms

    def calc(self):
        pass

    def draw(self):
        pass


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
