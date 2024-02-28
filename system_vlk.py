from PyQt5.uic.properties import QtCore
import drawer
from system import *
from candles import *


class TInfoMethod(TAnalysisMethod):
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
        pass
        for limit in self.candles.limits:
            drawer.fp.add_line((limit.candle0.ts, limit.value),
                               (limit.candle1.ts, limit.value), color='#FF00FF', width=4)

        # for candle in self.candles:
        #     if candle.uptake:
        #         drawer.fp.plot(candle.ts, candle.low, style='o', color='#A6FFA6')
        #         # todo plot рисует по 1 точке, а нужно серией?
        #     if candle.pushdown:
        #         drawer.fp.plot(candle.ts, candle.high, style='o', color='#FFA6A6')


class TMoneyMethod(TAnalysisMethod):
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
                        # drawer.fp.add_line((_ts+delta_ts, money.candle1.open),
                        #                    (_ts+delta_ts*3, money.candle1.open), color="CCFFCC", width=3)
                        drawer.fp.add_line((_ts, money.candle0.close),
                                           (self.ts_max(_ts + delta_ts * 3), money.candle0.close), color="59B359",
                                           width=1)
                        drawer.fp.add_rect((_ts, money.candle0.close),
                                           (_ts + delta_ts, max(money.candle1.low, money.candle0.low)), color="BFFFBF")

                    elif money.gap:
                        drawer.fp.add_line((_ts, money.candle0.close),
                                           (_ts + delta_ts + delta_ts, money.candle0.close), color="F2F200", width=1)
                        drawer.fp.add_rect((_ts, money.candle0.close),
                                           (_ts + delta_ts, money.candle1.open), color="FFFFBF")
                    # elif money.maker: drawer.fp.add_line((_ts, money.candle0.close), (self.ts_max(_ts+delta_ts*3),
                    # money.candle0.close), color="59B359", width=1) drawer.fp.add_rect((_ts, money.candle0.close),
                    # (_ts+delta_ts, max(money.candle1.low, money.candle0.low)), color="BFFFBF")

                else:  # dn
                    if money.limit or money.maker:
                        # drawer.fp.add_line((_ts+delta_ts, money.candle1.open),
                        #                    (_ts+delta_ts*3, money.candle1.open), color="FFBFBF", width=3)
                        drawer.fp.add_line((_ts, money.candle0.close),
                                           (self.ts_max(_ts + delta_ts * 3), money.candle0.close), color="D96C6C",
                                           width=1)
                        drawer.fp.add_rect((_ts, money.candle0.close),
                                           (_ts + delta_ts, min(money.candle1.high, money.candle0.high)),
                                           color="FFD9D9")

                    elif money.gap:
                        drawer.fp.add_line((_ts, money.candle0.close),
                                           (self.ts_max(_ts + delta_ts*2), money.candle0.close), color="F2F200", width=1)
                        drawer.fp.add_rect((_ts, money.candle0.close),
                                           (_ts + delta_ts, money.candle1.open), color="FFFFBF")
                    # elif money.maker: drawer.fp.add_line((_ts, money.candle0.close), (self.ts_max(_ts+delta_ts*3),
                    # money.candle0.close), color="D96C6C", width=1) drawer.fp.add_rect((_ts, money.candle0.close),
                    # (_ts+delta_ts, min(money.candle1.high, money.candle0.high)), color="FFD9D9")


class TStreamMethod(TAnalysisMethod):
    id = 'STREAM'

    def acalc(self):  # asinc
        pass

    def calc(self):

        c0 = self.candles[0]
        if self.candles[1].high < c0.high:
            self.candles.stream.append(TStreamItem(
                c0.ts, c0.high, 0, c0.ts, c0.high, 0, up=False, maxmin=c0.low))
        else:
            self.candles.stream.append(TStreamItem(
                c0.ts, c0.low, 0, c0.ts, c0.low, 0, up=True, maxmin=c0.high))

        i = 0
        while i < len(self.candles) - 1:
            ci = self.candles[i]
            ci1 = self.candles[i + 1]
            st = self.candles.stream[-1]

            if st.is_stop(ci, ci1):

                # расчет точки экстремума потока
                m = st.stop_value
                j = st.stop_index
                _ts = ci.ts
                _ii = j
                if st.up:  # up
                    while j <= i:  # + 1:
                        if self.candles[j].high > m:
                            m = self.candles[j].high
                            _ts = self.candles[j].ts
                            _ii = j
                        j += 1

                else:  # dn
                    while j <= i:  # + 1:
                        if self.candles[j].low < m:
                            m = self.candles[j].low
                            _ts = self.candles[j].ts
                            _ii = j
                        j += 1

                if self.candles.stream[-1].up:
                    if ci1.bullish and ci1.high > ci.high:  # то добавить  сразу 2 точки потока
                        self.candles.stream.append(TStreamItem(_ts, m, _ii, ci.ts, ci.low, i, up=False, maxmin=m))
                        self.candles.stream.append(
                            TStreamItem(ci1.ts, ci1.low, i + 1, ci.ts, ci.high, i, up=True, maxmin=m))
                    else:
                        if ci1.high > ci.high:
                            _ts = ci1.ts
                            m = ci1.high
                            _ii = i + 1

                        self.candles.stream.append(TStreamItem(
                            _ts, m, _ii, ci.ts, ci.low, i, up=False, maxmin=m))
                else:  # dn
                    if ci1.bearish and ci1.low < ci.low:  # то добавить  сразу 2 точки потока
                        self.candles.stream.append(TStreamItem(_ts, m, _ii, ci.ts, ci.high, i, up=True, maxmin=m))
                        self.candles.stream.append(
                            TStreamItem(ci1.ts, ci1.high, i + 1, ci.ts, ci.low, i, up=False, maxmin=m))
                    else:
                        if ci1.low < ci.low:
                            _ts = ci1.ts
                            m = ci1.low
                            _ii = i + 1

                        self.candles.stream.append(TStreamItem(
                            _ts, m, _ii, ci.ts, ci.high, i, up=True, maxmin=m))
            i += 1

    def draw(self):
        if len(self.candles.stream) > 2:
            delta_ts = self.candles[1].ts - self.candles[0].ts
            i = 0
            while i < len(self.candles.stream) - 1:
                # todo debug-mode: показывает точки остановки потока
                # drawer.fp.add_line(
                #     (self.stream[i].stop_ts, self.stream[i].stop_value),
                #     (self.stream[i].stop_ts + delta_ts/2, self.stream[i].stop_value),
                #     color="#bbb"
                # )
                drawer.fp.add_line(
                    (self.candles.stream[i].ts, self.candles.stream[i].value),
                    (self.candles.stream[i + 1].ts, self.candles.stream[i + 1].value),
                    color="#B9A6FF", width=1
                )
                i += 1


class TTendencyMethod(TAnalysisMethod):
    id = 'TENDENCY'

    def acalc(self):  # asinc  -- расчитывает например сразу появление 4ки и текущую свечу
        pass

    def calc(self):
        st = self.candles.stream
        tc = self.candles.tendency

        def recurcy(ep):  # ep - even point
            i = st.index(ep.si) + 1
            if i < len(st)-1:
                while i < len(st)-1 and tc.between_last2p(st[i]):
                    i += 1

                if tc.begin().si.up:
                    if st[i].value > ep.si.value:
                        recurcy(tc.add2p(ep, st.find_min(ep.si, st[i]), st[i]))
                    else:
                        recurcy(tc.enlarge(ep, st[i], ep.prev))
                else:  # dn
                    if st[i].value > ep.si.value:
                        recurcy(tc.enlarge(ep, st[i], ep.prev))
                    else:
                        recurcy(tc.add2p(ep, st.find_max(ep.si, st[i]), st[i]))

        recurcy(tc.start2p(st[0], st[1]))

        # todo recurcy(recurcy)

        if tc.between_last2p(tc[-1].si):
            tc[-1].si = tc[-2].si

    @staticmethod
    def color(p: TTendencyPoint):
        # todo config
        if p is None:
            return "eee"
        else:
            return "59B359" if p.si.up else "D96C6C"

    @staticmethod
    def title(p: TTendencyPoint):
        return '' if p.index == 1 else str(p.index)
        # if p.enlarge:
        #     return str(p.index)  # + "'" + str(p.range) + ", 1'" + str(p.range + 1)
        # else:
        #     return str(p.index)  # + "'" + str(p.range)

    def draw(self):  # todo debug-mode -- ? отображение надписей, в обыном режиме - рисовать
        tc = self.candles.tendency

        i = 0
        while i < len(tc)-1:
            drawer.fp.add_line(tc[i].coord(), tc[i+1].coord(), color="00FFF0")
            drawer.fp.add_text(tc[i].coord(), self.title(tc[i]), self.color(tc.begin(i-1)))  # color="eee")
            if tc[i].enlarge and i > 0:
                drawer.fp.add_line(tc[i-1].coord(), tc[i+1].coord(value=tc[i-1].si.value), color="ddd", width=1)
            i += 1

        # for p in tc:
        #     if p.index > 1:
        #         drawer.fp.add_text(p.coord(), self.title(p), self.color(tc.begin()))
        #
        # drawer.fp.add_line(tc[-2].coord(), tc[-1].coord(value=tc[-2].si.value), color="00FFF0", width=2)


# class TCorrectionMethod(TVolkMethod):
#

# tc.append(TTendencyNode(None, st[0]))  # point 1
# tc.append(TTendencyNode(None, st[1]))  # point 2
#
# if tc.between(st[2]):
#     tc.inside = TTendency()
#     tc.inside.append(TTendencyNode(tc, st[2]))
#     tc.inside.append(TTendencyNode(tc, st[3]))

#     def main(self):
#         logger.info(">> Volk system -- Correction Method start")
#
#

class TTemplateMethod(TAnalysisMethod):  # (SourceTrace)
    description = ['паттерны', '']
    citation = [' ... кто-то копит "шортистов"/"лонгистов" и с их подъсъема входим...']
    interpretation = []  # объяснение метода в диалоге с пользователем
    todo = ['на основании этого метода сделать мой метод пробой']
    pass


class TVlkSystem(TAnalysisSystem):
    def __init__(self, ms: TMetaSymbol, _drawer: TDrawer):
        super().__init__(ms, _drawer)
        logger.info(">> Vlk system init")

        self.methods.append(TInfoMethod(self.ms, self.ms.sT1.candles.day1))
        self.methods.append(TMoneyMethod(self.ms, self.ms.sT1.candles.day1))
        self.methods.append(TStreamMethod(self.ms, self.ms.sT1.candles.day1))
        self.methods.append(TTendencyMethod(self.ms, self.ms.sT1.candles.day1))

        # self.methods.append(TCorrectionMethod(self.ms))

    def main(self):
        self.ms.sT1.refresh()
        super().main()

        # # c0    c+1 !!! -- вперед + 1 надо смотреть!!! ###
        # def stream_stop(_item: TStreamItem, _c0, _c1: TCandle):
        #     if _item.up:
        #         return _c1.low < _c0.low
        #     else:
        #         return _c1.high > _c0.high
        #
        # # for zero point stream:
        # c0 = self.candles[0]
        # if self.candles[1].high < c0.high:
        #     self.stream.append(TStreamItem(c0.ts, c0.high, up=False, maxmin=c0.low))
        #     self.stream[-1].stop_value = c0.high
        # else:
        #     self.stream.append(TStreamItem(c0.ts, c0.low, up=True, maxmin=c0.high))
        #     self.stream[-1].stop_value = c0.low
        # self.stream[-1].stop_index = 0
        # self.stream[-1].stop_ts = c0.ts
        # self.stream[-1].next_ts = c0.ts
        #
        # i = 0
        # while i < len(self.candles) - 2:
        #     print(i)
        #     if stream_stop(self.stream[-1], self.candles[i], self.candles[i + 1]):
        #         # расчет точки остановки потока
        #         if self.stream[-1].up:
        #             stop_1 = self.candles[i].low
        #         else:
        #             stop_1 = self.candles[i].high
        #
        #         print('before', i, self.stream[-1].up)
        #         # пока добавляем, потом будем уточнять
        #         # if (not ((self.candles[i].bullish and self.candles[i + 1].bullish) or
        #         #          (self.candles[i].bearish and self.candles[i + 1].bearish))) and \
        #         #         (self.stream[-1].stop_index - i > 0):
        #         self.stream.append(TStreamItem(0, 0, up=not self.stream[-1].up))
        #         print('after add', i, self.stream[-1].up)
        #
        #         self.stream[-1].stop_index = i
        #         self.stream[-1].stop_ts = self.candles[i].ts
        #         self.stream[-1].stop_value = stop_1
        #         self.stream[-1].next_ts = self.candles[i + 1].ts
        #
        #         if len(self.stream) > 1 and self.stream[-1].stop_index - self.stream[-2].stop_index == 0:
        #             # если добавились две точки остановки потока на одной свече
        #             i += 1
        #
        #     else:
        #         i += 1
        #
        #
        #
        #

        # if stream_stop(self.stream[-1], self.candles[i], self.candles[i + 1]):
        #
        #     # if i > 0: i -= 1
        #
        #     # расчет точки остановки потока
        #     if self.stream[-1].up:
        #         stop_1 = self.candles[i].low
        #     else:
        #         stop_1 = self.candles[i].high
        #
        #     # расчет точки экстремума потока
        #     if self.stream[-1].up:
        #         # j = self.stream[-1].index + 1
        #         j = _last_stop_index
        #         _i = j
        #         while j <= i:  # + 1:  # нет! с + 1 не работает, ниже отдельно проверять
        #             if self.candles[j].high > self.stream[-1].maxmin:
        #                 self.stream[-1].maxmin = self.candles[j].high
        #                 _i = j
        #             j += 1
        #
        #     else:  # dn
        #         # j = self.stream[-1].index + 1
        #         j = _last_stop_index
        #         _i = j
        #         while j <= i:  # + 1:  # нет! с + 1 не работает, ниже отдельно проверять
        #             if self.candles[j].low < self.stream[-1].maxmin:
        #                 self.stream[-1].maxmin = self.candles[j].low
        #                 _i = j
        #             j += 1
        #
        #     _up = self.stream[-1].up
        #     _maxmin = self.stream[-1].maxmin
        #     _ts = self.candles[_i].ts
        #
        #     # уточнение точек экстремума
        #     # todo (i+1 и внутренние!!!)  # todo -- уточнить для bullish !!!!
        #     if _up \
        #             and self.candles[i + 1].bearish \
        #             and self.candles[i + 1].high > _maxmin:
        #         # print(i + 1, _maxmin, self.candles[i + 1].high)
        #         _maxmin = self.candles[i + 1].high
        #         _ts = self.candles[i + 1].ts
        #         _i = i + 1
        #     if not _up \
        #             and self.candles[i + 1].bullish \
        #             and self.candles[i + 1].low < _maxmin:
        #         # print(i + 1, _maxmin, self.candles[i + 1].low)
        #         _maxmin = self.candles[i + 1].low
        #         _ts = self.candles[i + 1].ts
        #         _i = i + 1
        #
        #     # добавить точку экстремума потока
        #     item = TStreamItem(_ts,
        #                        _maxmin,
        #                        _i,
        #                        up=not self.stream[-1].up,  # направление противоположное посл точке потока
        #                        maxmin=_maxmin)
        #     self.stream.append(item)
        #
        #     # добавить точку остановки потока в запись точки экстремума потока (после нахождения экстремума !)
        #     # не перемещать этот блок выше!
        #     self.stream[-1].stop_index = i
        #     self.stream[-1].stop_ts = self.candles[i].ts
        #     self.stream[-1].stop_value = stop_1
        #     _last_stop_index = i
        #
        # i += 1

        # while i < 30:  # len(self.candles) - 1:
        #
        #     if stream_stop(self.stream[-1], self.candles[i], self.candles[i + 1]):
        #         print(i)
        #         self.stream.append(
        #             TStreamItem(self.candles[self.stream[-1].index],
        #                         self.stream[-1].maxmin,
        #                         self.stream[-1].index,
        #                         up=not self.stream[-1].up))  # направление противоположное посл точке потока
        #     else:
        #         if self.stream[-1].up:
        #             # self.stream[-1].maxmin = max(self.stream[-1].maxmin, self.candles[i].high)  # нихуя!
        #             if self.candles[i].high > self.stream[-1].maxmin:
        #                 self.stream[-1].maxmin = self.candles[i].high
        #                 self.stream[-1].index = i
        #         else:
        #             if self.candles[i].low < self.stream[-1].maxmin:
        #                 self.stream[-1].maxmin = self.candles[i].low
        #                 self.stream[-1].index = i
        #     i += 1

# if self.stream[-1].up:
#     maxmin = max(maxmin, self.candles[i].high)
#     if maxmin != self.candles[i].high: _i = i
# else:
#     maxmin = min(maxmin, self.candles[i].low)
#     if maxmin != self.candles[i].low: _i = i


# ts = self.candles[i].ts
# if self.stream[-1].up:
#     if self.candles[i + 1].high > self.candles[i].high:
#         ts = self.candles[i + 1].ts
#         maxmin = max(maxmin, self.candles[i].high)
#         i += 1
#     else:
#         ts = self.candles[i].ts
# else:
#     if self.candles[i + 1].low < self.candles[i].low:
#         ts = self.candles[i + 1].ts
#         maxmin = min(maxmin, self.candles[i].low)
#         i += 1
#     else:
#         ts = self.candles[i].ts
# дополнительно проверяем i+1 свечу  todo -- проверять серию внутренних свечей
# if self.stream[-1].up and self.candles[i+1].bearish \
#         and self.candles[i + 1].high > self.stream[-1].maxmin:
#     self.stream[-1].maxmin = self.candles[i + 1].high
#     _i = i+1

# if not self.stream[-1].up and self.candles[i+1].bullish \
#         and self.candles[i + 1].low < self.stream[-1].maxmin:
#     self.stream[-1].maxmin = self.candles[i + 1].low
#     _i = i+1


# def find_rs(self, from_index):  # найти РЕЗУЛЬТАТИВНЫЙ ПОТОК, начиная с индека потока
#     i = from_index
#     r = 0
#     while i < len(self.candles.stream)-3:
#         p1 = self.candles.stream[i]
#         p2 = self.candles.stream[i+1]
#         p3 = self.candles.stream[i+2]
#         p4 = self.candles.stream[i+3]
#
#         if (p1.up and p4.value > p2.value) or (not p1.up and p4.value < p2.value):
#             # r = p3.index  # это индекс свечи, неправильно!
#             r = i+2  # вернкть индекс в потоке 3ей точки
#             break
#
#         i += 1
#
#     return r

# def find_segment(self, tn: TTendencyPoint):
#     pass
