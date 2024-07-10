import drawer
from system.abstract import *


class InfoMethod(AnalysisMethod):
    id = 'BASEINFO'
    description = ['Candles Info Method',
                   'UpTake/PushDown candles',
                   'for _Buyer/for _Seller candles)',
                   'Limits (wick, body, close/open and for more candles)']

    def calc(self):
        # limits, so far, only 2 point
        # todo: сделать распознавание лимиток дальше чем 2 ближ свечи (позже)
        if len(self.candles) > 2:
            i = 1
            while i < len(self.candles):
                # todo проверить свечи итерирую от а=первой к последней, а когда писал код,
                # todo было чувство как в пайн-скрипт, короче проверить
                c0 = self.candles[i]
                c_1 = self.candles[i - 1]  # c_1 == c-1

                if (c0.high > c_1.high) and (c0.low < c_1.low):  # todo открытие тоже должно быть выше???
                    if c0.bullish: c0.uptake = True
                    if c0.bearish: c0.pushdown = True

                # if c0.bearish and c0.open > c_1.close and c0.close < c_1.open: c0.pushdown = True

                # todo:
                # for_buyer: False
                # for_seller: False

                if c0.high == c_1.high:
                    self.candles.limits.append(TLimit(c0, c_1, c0.high, wick=True, up=True))

                if c0.low == c_1.low:
                    self.candles.limits.append(TLimit(c0, c_1, c0.low, wick=True, dn=True))

                if c0.body_max == c_1.body_max:
                    self.candles.limits.append(TLimit(c0, c_1, c0.body_max, body=True, up=True))

                if c0.body_min == c_1.body_min:
                    self.candles.limits.append(TLimit(c0, c_1, c0.body_min, body=True, dn=True))

                if c_1.close == c0.open:
                    self.candles.limits.append(TLimit(c0, c_1, c_1.close, co=True))

                i += 1  # ! while

    def draw(self):
        for limit in self.candles.limits:
            drawer.fp.add_line((limit.candle0.ts, limit.value),
                                (limit.candle1.ts, limit.value), color=cLimit, width=4, ax=self.ax)

            # for candle in self.candles:
            #     if candle.uptake:
            #         drawer.fp.plot(candle.ts, candle.low, style='o', color='#A6FFA6')
            #         # todo plot рисует по 1 точке, а нужно серией?
            #     if candle.pushdown:
            #         drawer.fp.plot(candle.ts, candle.high, style='o', color='#FFA6A6')