import drawer
from system import *
from candles import *


class TCandlesInfoMethod(TAnalysisMethod):
    description = ['Base system -- Candles Info Method']

    def calc(self):

        # limits, so far, only 2 point
        if len(self.candles) > 2:
            i = 1
            while i < len(self.candles):
                c0 = self.candles[i - 1]
                c1 = self.candles[i]

                # todo: realise from **kwarg!!! in __init()__
                if c0.high == c1.high:
                    limit = TLimit(c0, c1)
                    limit.set_up(c0.high)
                    self.candles.limits.append(limit)

                if c0.low == c1.low:
                    limit = TLimit(c0, c1)
                    limit.set_dn(c0.low)
                    self.candles.limits.append(limit)

                if c0.body_max == c1.body_max:
                    limit = TLimit(c0, c1)
                    limit.set_up_body(c0.body_max)
                    self.candles.limits.append(limit)

                if c0.body_min == c1.body_min:
                    limit = TLimit(c0, c1)
                    limit.set_dn_body(c0.body_min)
                    self.candles.limits.append(limit)

                i += 1

    def draw(self):
        for limit in self.candles.limits:
            self.drawer.add_limit(limit.candle0.ts, limit.candle1.ts, limit.value)

