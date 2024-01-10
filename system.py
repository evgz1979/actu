from symbols import *


class TAnalysisMethod:
    pass


class TAnalysisSystem:
    ms: TMetaSymbol
    methods: [TAnalysisMethod]

    def __init__(self, ms: TMetaSymbol):
        self.ms = ms


class TMetaSystem:
    pass
