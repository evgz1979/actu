import drawer
from system.abstract import *


class MoneyMethod(AnalysisMethod):
    id = 'MONEY'

    def calc(self):
        if len(self.candles) > 2:
            i = 0
            while i < len(self.candles) - 1:
                ci = self.candles[i]
                ci1 = self.candles[i + 1]

                if (ci.bullish or ci.flat) and (ci1.bullish or ci1.flat) and (
                        not (ci.flat and ci1.flat)) and ci1.high > ci.high:
                    if ci1.open > ci.close:
                        self.candles.moneys.append(TMoney(ci, ci1, up=True, gap=True))
                    else:
                        self.candles.moneys.append(TMoney(ci, ci1, up=True, maker=True))

                if (ci.bearish or ci.flat) and (ci1.bearish or ci1.flat) and (
                        not (ci.flat and ci1.flat)) and ci1.low < ci.low:
                    if ci1.open < ci.close:
                        self.candles.moneys.append(TMoney(ci, ci1, dn=True, gap=True))
                    # todo ??? elif ci1.high <= ci.high:
                    else:
                        self.candles.moneys.append(TMoney(ci, ci1, dn=True, maker=True))

                i += 1  # ! while

    def draw(self):
        delta_ts = self.candles[1].ts - self.candles[0].ts

        if len(self.candles.moneys) > 1:

            for money in self.candles.moneys:
                _ts = money.candle0.ts

                if money.up:
                    if money.limit or money.maker:
                        # old---drawer.fp.add_line((_ts+delta_ts, money.candle1.open),
                        #                    (_ts+delta_ts*3, money.candle1.open), color="CCFFCC", width=3)

                        drawer.fp.add_line((_ts, money.candle0.close),
                                           (self.ts_max(_ts + delta_ts * 2), money.candle0.close), color="59B359",
                                           width=1, ax=self.ax)
                        drawer.fp.add_rect((_ts, money.candle0.close),
                                           (_ts + delta_ts, max(money.candle1.low, money.candle0.low)),
                                           color="BFFFBF", ax=self.ax)

                    elif money.gap:
                        drawer.fp.add_line((_ts, money.candle0.close),
                                           (self.ts_max(_ts + delta_ts * 2), money.candle0.close), color="F2F200",
                                           width=1, ax=self.ax)
                        drawer.fp.add_rect((_ts, money.candle0.close),
                                           (_ts + delta_ts, money.candle1.open), color="FFFFBF", ax=self.ax)
                    # elif money.maker: drawer.fp.add_line((_ts, money.candle0.close), (self.ts_max(_ts+delta_ts*3),
                    # money.candle0.close), color="59B359", width=1) drawer.fp.add_rect((_ts, money.candle0.close),
                    # (_ts+delta_ts, max(money.candle1.low, money.candle0.low)), color="BFFFBF")

                else:  # dn
                    if money.limit or money.maker:
                        # old---drawer.fp.add_line((_ts+delta_ts, money.candle1.open),
                        #                    (_ts+delta_ts*3, money.candle1.open), color="FFBFBF", width=3)

                        drawer.fp.add_line((_ts, money.candle0.close),
                                           (self.ts_max(_ts + delta_ts * 2), money.candle0.close), color="D96C6C",
                                           width=1, ax=self.ax)
                        drawer.fp.add_rect((_ts, money.candle0.close),
                                           (self.ts_max(_ts + delta_ts), min(money.candle1.high, money.candle0.high)),
                                           color="FFD9D9", ax=self.ax)

                    elif money.gap:
                        drawer.fp.add_line((_ts, money.candle0.close),
                                           (self.ts_max(_ts + delta_ts * 2), money.candle0.close), color="F2F200",
                                           width=1, ax=self.ax)
                        drawer.fp.add_rect((_ts, money.candle0.close),
                                           (self.ts_max(_ts + delta_ts), money.candle1.open), color="FFFFBF", ax=self.ax)
                    # elif money.maker: drawer.fp.add_line((_ts, money.candle0.close), (self.ts_max(_ts+delta_ts*3),
                    # money.candle0.close), color="D96C6C", width=1) drawer.fp.add_rect((_ts, money.candle0.close),
                    # (_ts+delta_ts, min(money.candle1.high, money.candle0.high)), color="FFD9D9")