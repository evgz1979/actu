from symbols import *


class TAnalysisMethod:
    ms: TMetaSymbol

    def __init__(self, ms: TMetaSymbol):
        self.ms = ms

    def main(self):
        pass

    def calc(self, candles: TCandlesList):
        pass

    def draw(self):
        pass


class TAnalysisSystem:
    ms: TMetaSymbol
    methods = []

    def __init__(self, ms: TMetaSymbol):
        self.ms = ms

    def main(self):
        for m in self.methods:
            m.main()

    def draw(self):
        for m in self.methods:
            m.main()

    async def amain(self):
        pass


class TBaseSystem:
    pass


class TMetaSystem:
    pass
