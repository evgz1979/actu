from symbols import *


class TAnalysisMethod:
    def main(self):
        pass


class TAnalysisSystem:
    ms: TMetaSymbol
    methods = []

    def __init__(self, ms: TMetaSymbol):
        self.ms = ms

    def main(self):
        for m in self.methods:
            m.main()

    async def amain(self):
        pass


class TBaseSystem:
    pass


class TMetaSystem:
    pass
