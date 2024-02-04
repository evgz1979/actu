from system import *
from candles import *


class TCandlesInfoMethod(TAnalysisMethod):

    def calc(self, candles: TCandlesList):

        # limits, so far, only 2 point
        if len(candles) > 2:
            i = 1
            while i < len(candles):
                c0 = candles[i - 1]
                c1 = candles[i]

                if c0.high == c1.high: candles.limits.set_up(c0, c1)
                if c0.low == c1.low: candles.limits.set_dn(c0, c1)
                if c0.body_max == c1.body_max: candles.limits.set_up_body(c0, c1)
                if c0.body_min == c1.body_min: candles.limits.set_dn_body(c0, c1)

                i += 1

    def main(self):
        logger.info(">> Base system -- Candles Info Method start")

        self.ms.spot_T0.refresh()
        self.calc(self.ms.spot_T0.candles.day1)

