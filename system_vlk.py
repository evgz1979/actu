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
        if self.visible:
            for limit in self.candles.limits:
                drawer.fp.add_line((limit.candle0.ts, limit.value),
                                   (limit.candle1.ts, limit.value), color='#FF00FF', width=4, ax=self.ax)

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

        if not self.visible: return

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
                                           width=1, ax=self.ax)
                        drawer.fp.add_rect((_ts, money.candle0.close),
                                           (_ts + delta_ts, max(money.candle1.low, money.candle0.low)),
                                           color="BFFFBF", ax=self.ax)

                    elif money.gap:
                        drawer.fp.add_line((_ts, money.candle0.close),
                                           (self.ts_max(_ts + delta_ts*2), money.candle0.close), color="F2F200",
                                           width=1, ax=self.ax)
                        drawer.fp.add_rect((_ts, money.candle0.close),
                                           (_ts + delta_ts, money.candle1.open), color="FFFFBF", ax=self.ax)
                    # elif money.maker: drawer.fp.add_line((_ts, money.candle0.close), (self.ts_max(_ts+delta_ts*3),
                    # money.candle0.close), color="59B359", width=1) drawer.fp.add_rect((_ts, money.candle0.close),
                    # (_ts+delta_ts, max(money.candle1.low, money.candle0.low)), color="BFFFBF")

                else:  # dn
                    if money.limit or money.maker:
                        # drawer.fp.add_line((_ts+delta_ts, money.candle1.open),
                        #                    (_ts+delta_ts*3, money.candle1.open), color="FFBFBF", width=3)
                        drawer.fp.add_line((_ts, money.candle0.close),
                                           (self.ts_max(_ts + delta_ts * 3), money.candle0.close), color="D96C6C",
                                           width=1, ax=self.ax)
                        drawer.fp.add_rect((_ts, money.candle0.close),
                                           (_ts + delta_ts, min(money.candle1.high, money.candle0.high)),
                                           color="FFD9D9", ax=self.ax)

                    elif money.gap:
                        drawer.fp.add_line((_ts, money.candle0.close),
                                           (self.ts_max(_ts + delta_ts*2), money.candle0.close), color="F2F200",
                                           width=1, ax=self.ax)
                        drawer.fp.add_rect((_ts, money.candle0.close),
                                           (_ts + delta_ts, money.candle1.open), color="FFFFBF", ax=self.ax)
                    # elif money.maker: drawer.fp.add_line((_ts, money.candle0.close), (self.ts_max(_ts+delta_ts*3),
                    # money.candle0.close), color="D96C6C", width=1) drawer.fp.add_rect((_ts, money.candle0.close),
                    # (_ts+delta_ts, min(money.candle1.high, money.candle0.high)), color="FFD9D9")


# class TStreamZeroMethod(TAnalysisMethod):
#     id = 'STREAM0'
#
#     def calc(self):
#         st = self.candles.stream0
#         c = self.candles
#
#         i = 0
#         while i < len(c)-1:
#             st.append(TStreamItem(c[i].enter, c[i].exit))
#             if
#             st.append(TStreamItem(c[i].exit, c[i+1].enter))
#             i += 1
#
#     def draw(self):
#         if not self.visible: return
#         st = self.candles.stream0
#
#         i = 0
#         while i < len(st) - 1:
#             drawer.fp.add_line(st[i].enter, st[i].exit, color="#B9A6FF", width=3, ax=self.ax)
#             i += 1


class TStreamMethod(TAnalysisMethod):
    id = 'STREAM'

    # def calc(self):
    #
    #     c0 = self.candles[0]
    #     if self.candles[1].high < c0.high:
    #         self.candles.stream.append(TStreamItem(
    #             c0.ts, c0.high, 0, c0.ts, c0.high, 0, up=False, maxmin=c0.low))
    #     else:
    #         self.candles.stream.append(TStreamItem(
    #             c0.ts, c0.low, 0, c0.ts, c0.low, 0, up=True, maxmin=c0.high))
    #
    #     i = 0
    #     while i < len(self.candles) - 1:
    #         ci = self.candles[i]
    #         ci1 = self.candles[i + 1]
    #         st = self.candles.stream[-1]
    #
    #         if st.is_stop(ci, ci1):
    #
    #             # расчет точки экстремума потока
    #             m = st.stop_value
    #             j = st.stop_index
    #             _ts = ci.ts
    #             _ii = j
    #             if st.up:  # up
    #                 while j <= i:  # + 1:
    #                     if self.candles[j].high > m:
    #                         m = self.candles[j].high
    #                         _ts = self.candles[j].ts
    #                         _ii = j
    #                     j += 1
    #
    #             else:  # dn
    #                 while j <= i:  # + 1:
    #                     if self.candles[j].low < m:
    #                         m = self.candles[j].low
    #                         _ts = self.candles[j].ts
    #                         _ii = j
    #                     j += 1
    #
    #             if self.candles.stream[-1].up:
    #                 if ci1.bullish and ci1.high > ci.high:  # то добавить  сразу 2 точки потока
    #                     self.candles.stream.append(TStreamItem(_ts, m, _ii, ci.ts, ci.low, i, up=False, maxmin=m))
    #                     self.candles.stream.append(
    #                         TStreamItem(ci1.ts, ci1.low, i + 1, ci.ts, ci.high, i, up=True, maxmin=m))
    #                 else:
    #                     if ci1.high > ci.high:
    #                         _ts = ci1.ts
    #                         m = ci1.high
    #                         _ii = i + 1
    #
    #                     self.candles.stream.append(TStreamItem(
    #                         _ts, m, _ii, ci.ts, ci.low, i, up=False, maxmin=m))
    #             else:  # dn
    #                 if ci1.bearish and ci1.low < ci.low:  # то добавить  сразу 2 точки потока
    #                     self.candles.stream.append(TStreamItem(_ts, m, _ii, ci.ts, ci.high, i, up=True, maxmin=m))
    #                     self.candles.stream.append(
    #                         TStreamItem(ci1.ts, ci1.high, i + 1, ci.ts, ci.low, i, up=False, maxmin=m))
    #                 else:
    #                     if ci1.low < ci.low:
    #                         _ts = ci1.ts
    #                         m = ci1.low
    #                         _ii = i + 1
    #
    #                     self.candles.stream.append(TStreamItem(
    #                         _ts, m, _ii, ci.ts, ci.high, i, up=True, maxmin=m))
    #         i += 1

    def find_extr(self, i, st: TStreamItem):  # todo -> stream
        m = st.stop_value
        j = st.stop_index
        _ts = self.candles[i].ts
        _ii = j
        if st.up:  # up
            while j <= i + 1:
                if self.candles[j].high > m:
                    m = self.candles[j].high
                    _ts = self.candles[j].ts
                    _ii = j
                j += 1

        else:  # dn
            while j <= i + 1:
                if self.candles[j].low < m:
                    m = self.candles[j].low
                    _ts = self.candles[j].ts
                    _ii = j
                j += 1
        return m, _ts, _ii

    def find_extr_invert(self, i, st: TStreamItem):  # todo -> stream
        m = st.stop_value
        j = st.stop_index
        _ts = self.candles[i].ts
        _ii = j
        if st.up:  # up
            m = self.candles[i].high
            _ts = self.candles[i].ts
            _ii = i
        else:  # dn
            m = self.candles[i].low
            _ts = self.candles[i].ts
            _ii = i
        return m, _ts, _ii

    # def calc(self):  # ver 0.2
    #
    #     c0 = self.candles[0]
    #     if self.candles[1].high < c0.high:
    #         self.candles.stream.append(TStreamItem(
    #             c0.ts, c0.high, 0, c0.ts, c0.high, 0, up=False, maxmin=c0.low))
    #     else:
    #         self.candles.stream.append(TStreamItem(
    #             c0.ts, c0.low, 0, c0.ts, c0.low, 0, up=True, maxmin=c0.high))
    #
    #     i = 0
    #     while i < len(self.candles) - 1:
    #         ci = self.candles[i]
    #         ci1 = self.candles[i + 1]
    #         st = self.candles.stream[-1]
    #
    #         if st.is_stop(ci, ci1):
    #             m, _ts, _ii = self.find_extr(i, st)
    #             self.candles.stream.append(TStreamItem(
    #                 _ts, m, _ii, ci.ts, st.get_stop(ci, ci1), i, up=not st.up, maxmin=m))
    #             print('append', _ii, 'for stop point', i, not st.up)
    #
    #             # внутри вернехого if !!! - то есть после того, как добавили
    #             st1 = self.candles.stream[-1]
    #             # если еще на этойже свече есть остановка потока в другую сторону
    #             if st1.is_stop(ci, ci1) and st1.index != i and st1.index != i+1:  # todo add V-pattern ?
    #                 # print('inside', i, st1.up)
    #
    #                 m, _ts, _ii = self.find_extr_invert(i, st1)
    #
    #                 self.candles.stream.append(TStreamItem(
    #                     _ts, m, _ii, ci.ts, st1.get_stop(ci, ci1), i, up=not st1.up, maxmin=m))
    #                 print('append inside', _ii, 'for stop point', i, not st1.up)
    #
    #                 st2 = self.candles.stream[-1]
    #                 m, _ts, _ii = self.find_extr_invert(i+1, st2)
    #                 self.candles.stream.append(TStreamItem(
    #                     _ts, m, _ii, ci.ts, st1.get_stop(ci, ci1), i, up=not st2.up, maxmin=m))
    #                 print('append inside', _ii, 'for stop point', i, not st2.up)
    #
    #         i += 1

    def calc(self):  # ver 0.5
        i = 0
        c = self.candles

        def level0():
            st.append(TStreamItem(c[i].enter, c[i].exit))
            st.append(TStreamItem(c[i].exit, c[i+1].enter))

        def level1():
            if len(st) > 0 and st[-1].is_beetwin(c[i], c[i + 1]):
                st.append(TStreamItem(c[i].enter, c[i+1].enter))
            elif len(st) > 0 and st[-1].is_correction(c[i], c[i + 1]):
                st.append(TStreamItem(c[i].enter, c[i+1].enter))
            else:
                level0()

        st = self.candles.stream0  # Stream Zero Level
        i = 0
        while i < len(c)-1:
            level0()
            i += 1

        st = self.candles.stream1  # Stream Level 1
        i = 0
        while i < len(c)-1:
            level1()
            i += 1
        st.normalize()

        # st = self.candles.stream  # Base Stream
        #
        # i = 0
        # while i < len(c)-1:
        #     if len(st) > 0 and st[-1].is_beetwin(c[i], c[i + 1]):
        #         st.append(TStreamItem(c[i].enter, c[i+1].enter))
        #     elif len(st) > 0 and st[-1].is_correction(c[i], c[i + 1]):
        #         st.append(TStreamItem(c[i].enter, c[i+1].enter))
        #     else:
        #         st.append(TStreamItem(c[i].enter, c[i].exit))
        #         st.append(TStreamItem(c[i].exit, c[i + 1].enter))
        #     i += 1
        #
        # st.normalize()


        # st = self.candles.stream
        # c = self.candles
        # st.append(TStreamItem(c[0].enter, c[0].exit, c[0].enter))

        # i = 0
        # while i < len(c) - 1:
        #     st[-1].move_exit(c[i])  # сместить экстремум
        #
        #     if st[-1].is_stop(c[i+1]):  # todo перед добавлением проверять со второй стороны!! ??
        #
        #         # st[-1].move_exit(c[i+1])
        #         st.append(TStreamItem(st[-1].exit, c[i+1].exit, c[i+1].enter))
        #         if i < 25: print('append for stop=', i)
        #     else: st[-1].move_stop(c[i+1])
        #     i += 1

        # i = 0
        # while i < len(c) - 1:
        #     st.append(TStreamItem(c[i].enter, c[i].exit))
        #     st.append(TStreamItem(c[i].exit, c[i+1].enter))
        #     i += 1


    def draw(self):
        if not self.visible: return

        for st in self.candles.stream0:
            drawer.fp.add_line(st.enter, st.exit, color="#B9A6FF", width=1, ax=self.ax)

        for st in self.candles.stream1:
            drawer.fp.add_line(st.enter, st.exit, color="#B9A6FF", width=2, ax=self.ax)

        # for st in self.candles.stream:
        #     drawer.fp.add_line(st.enter, st.exit, color="#B9A6FF", width=3, ax=self.ax)

        # if not self.visible: return
        # st = self.candles.stream
        # c = self.candles
        #
        # i = 0
        # while i < len(st) - 1:
        #     # drawer.fp.add_line(c.dts(st[i].stop, -0.5), c.dts(st[i].stop, 0.5), width=3, ax=self.ax)
        #     drawer.fp.add_line(st[i].enter, st[i].exit, color="#B9A6FF", width=3, ax=self.ax)
        #     # drawer.fp.add_text(st[i].enter, 'ˆ' if st[i].up else 'v')
        #     i += 1




class TTendencyMethod(TAnalysisMethod):
    id = 'TENDENCY'

    def acalc(self):  # asinc  -- расчитывает например сразу появление 4ки и текущую свечу
        pass

    def calc(self):
        st = self.candles.stream
        tc = self.candles.tendency

        # def recurcy(ep):  # ep - even point
        #     i = st.index(ep.si) + 1
        #     if i < len(st)-1:
        #         while i < len(st)-1 and tc.between_last2p(st[i]):
        #             i += 1
        #
        #         if tc.begin().si.up:
        #             if st[i].value > ep.si.value:
        #                 recurcy(tc.add2p(ep, st.find_min(ep.si, st[i]), st[i]))
        #             else:
        #                 recurcy(tc.enlarge(ep, st[i], ep.prev))
        #         else:  # dn
        #             if st[i].value > ep.si.value:
        #                 recurcy(tc.enlarge(ep, st[i], ep.prev))
        #             else:
        #                 recurcy(tc.add2p(ep, st.find_max(ep.si, st[i]), st[i]))
        #
        # recurcy(tc.start2p(st[0], st[1]))
        #
        # # todo recurcy(recurcy)
        #
        # if tc.between_last2p(tc[-1].si):
        #     tc[-1].si = tc[-2].si

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
        if not self.visible: return
        # tc = self.candles.tendency
        #
        # i = 0
        # while i < len(tc)-1:
        #     drawer.fp.add_line(tc[i].coord(), tc[i+1].coord(), color="00FFF0", ax=self.ax)
        #     drawer.fp.add_text(tc[i].coord(), self.title(tc[i]), self.color(tc.begin(i-1)), ax=self.ax)  # color="eee")
        #     if tc[i].enlarge and i > 0:
        #         drawer.fp.add_line(tc[i-1].coord(), tc[i+1].coord(value=tc[i-1].si.value), color="ddd",
        #                            width=1, ax=self.ax)
        #     i += 1


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

    def add_methods(self, interval: Interval, _ax):
        d = self.ms.future.candles.get(interval)
        self.methods.append(TInfoMethod(self.ms, d, _ax, visible=False))
        self.methods.append(TMoneyMethod(self.ms, d, _ax, visible=False))
        # self.methods.append(TStreamZeroMethod(self.ms, d, _ax))
        self.methods.append(TStreamMethod(self.ms, d, _ax))
        self.methods.append(TTendencyMethod(self.ms, d, _ax, visible=False))

        # self.methods.append(TCorrectionMethod(self.ms))

    def main(self):
        # self.ms.spotT1.refresh()
        self.ms.future.refresh()
        super().main()

