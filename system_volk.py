from symbols import *
from system import *
from candles import *


class TCandlesInfoMethod(TAnalysisMethod):  # -> system.py  --> BaseSystem
    ms: TMetaSymbol
    limits = [T2Candles]

    def __init__(self, ms: TMetaSymbol):
        self.ms = ms

    def calc(self, candles: TCandles):
        pass

    def main(self):
        logger.info(">> Base system -- Candles Info Method start")

        self.calc(self.ms.spot_T0.candles.day1)


class TSignOfMoneyMethod(TAnalysisMethod):
    ms: TMetaSymbol

    def __init__(self, ms: TMetaSymbol):
        self.ms = ms

    def calc(self, candles: TCandles):
        pass

    def main(self):
        logger.info(">> Volk system -- SignOfMoney Method start")

        self.calc(self.ms.spot_T0.candles.day1)


class TTendencyMethod(TAnalysisMethod):
    ms: TMetaSymbol

    def __init__(self, ms: TMetaSymbol):
        self.ms = ms

    def calc(self, candles: TCandles):
        pass

    def main(self):
        logger.info(">> Volk system -- Tendency Method start")

        self.calc(self.ms.spot_T0.candles.day1)


class TCorrectionMethod(TAnalysisMethod):
    pass


class TTimeFramesRelationsMethod(TAnalysisMethod):
    pass


class TVolkSystem(TAnalysisSystem):
    def __init__(self, ms: TMetaSymbol):
        super().__init__(ms)
        logger.info(">> Volk system init")

        self.methods.append(TCandlesInfoMethod(self.ms))
        self.methods.append(TSignOfMoneyMethod(self.ms))
        self.methods.append(TTendencyMethod(self.ms))
