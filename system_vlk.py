from PyQt5.uic.properties import QtCore
import drawer
from system import *
from candles import *
from system_flow import *


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
                                           (self.ts_max(_ts + delta_ts * 2), money.candle0.close), color="F2F200",
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
                                           (self.ts_max(_ts + delta_ts * 2), money.candle0.close), color="F2F200",
                                           width=1, ax=self.ax)
                        drawer.fp.add_rect((_ts, money.candle0.close),
                                           (_ts + delta_ts, money.candle1.open), color="FFFFBF", ax=self.ax)
                    # elif money.maker: drawer.fp.add_line((_ts, money.candle0.close), (self.ts_max(_ts+delta_ts*3),
                    # money.candle0.close), color="D96C6C", width=1) drawer.fp.add_rect((_ts, money.candle0.close),
                    # (_ts+delta_ts, min(money.candle1.high, money.candle0.high)), color="FFD9D9")


class TTemplateMethod(TAnalysisMethod):  # (SourceTrace)
    description = ['паттерны', '']
    citation = [' ... кто-то копит "шортистов"/"лонгистов" и с их подъсъема входим...']
    interpretation = []  # объяснение метода в диалоге с пользователем
    todo = ['на основании этого метода сделать мой метод пробой']
    pass


class TStreamMethod(TAnalysisMethod):
    id = 'STREAM'

    @staticmethod
    def is_correction(ci, ci1: TCandle):
        return (ci.enter[1] <= ci1.low <= ci.exit[1] < ci1.high) or (
                ci.enter[1] >= ci1.high >= ci.exit[1] > ci1.low)

    def level0(self, st: TStream):
        c = self.candles
        i = 0
        while i < len(c) - 1:
            st.append(TStreamItem(c[i].enter, c[i].exit, visible=False))
            st.append(TStreamItem(c[i].exit, c[i + 1].enter, visible=False))
            i += 1

    def level1(self, st: TStream):
        c = self.candles
        i = 0
        while i < len(c) - 1:
            if len(st) > 0 and self.is_correction(c[i], c[i + 1]):
                st.append(TStreamItem(c[i].enter, c[i + 1].enter, visible=False))
            # elif len(st) > 0 and self.is_merge_wicks(c[i], c[i + 1]):
            else:
                # level0(st)
                st.append(TStreamItem(c[i].enter, c[i].exit, visible=False))
                st.append(TStreamItem(c[i].exit, c[i + 1].enter, visible=False))
            i += 1

    def level_base_0_7(self, st: TStream):  # ver 0.7
        c = self.candles
        st.append(TStreamItem(c[0].enter, c[0].exit, c[0].enter))

        p = False  # pass
        i = 0
        while i < len(c) - 1:

            if st[-1].is_stop2(c[i], c[i + 1]):

                ex = st[-1].get_exit(c[i + 1])

                if st[-1].up:
                    if c[i + 1].high > st[-1].exit[1]:
                        if c[i + 1].bearish:
                            st[-1].exit = c[i + 1].enter

                        else:  # c[i+1].bullish:
                            st.append(TStreamItem(st[-1].exit, c[i + 1].enter))
                            st.append(TStreamItem(c[i + 1].enter, c[i + 1].exit))
                            ex = c[i + 1].exit
                    else:  # c[i+1].high <= st[-1].exit[1]:   # todo error !!! on candle 2024-01-04
                        if c[i + 1].bearish and st[-1].exit[0] < c[i].ts:
                            st.append(TStreamItem(st[-1].exit, c[i].enter))
                            st.append(TStreamItem(c[i].enter, c[i + 1].enter))
                            ex = c[i + 1].exit
                        # else:
                        #     p = True

                else:  # dn
                    if c[i + 1].low < st[-1].exit[1]:
                        if c[i + 1].bullish:
                            st[-1].exit = c[i + 1].enter

                        # else:   # c[i + 1].bearish

                # if st[-1].exit[1] == ex[1]:
                #     pass
                # else:

                # if p:
                #     p = False
                # else:
                st.append(TStreamItem(st[-1].exit, ex, st[-1].get_stop(c[i])))

            else:
                st[-1].move_exit(c[i], c[i + 1])

            i += 1

            # self.candles.stream.normalize()  todo ???

    def level_base_0_8(self, st: TStream):  # ver 0.7
        c = self.candles
        st.append(TStreamItem(c[0].enter, c[0].exit, c[0].enter))

        i = 0
        while i < len(c) - 1:
            st[-1].move_exit(c[i], c[i + 1])
            ex = st[-1].get_exit(c[i + 1])

            if st[-1].is_stop2(c[i], c[i + 1]):
                st.append(TStreamItem(st[-1].exit, ex, st[-1].get_stop(c[i])))

            i += 1

    def level2(self, st: TStream):
        c = self.candles
        st1 = self.candles.stream1
        st.append(TStreamItem(st1[0].enter, st1[0].enter, st1[0].enter))

        i = 0
        while i < len(c) - 1:
            # if st[-1].is_stop2(c[i], c[i + 1]):
            #     st.append(TStreamItem(
            #         st[-1].exit,
            #         st1.get_exit(st[-1], c[i], c[i + 1]),
            #         st[-1].get_stop(c[i])))
            i += 1

    def calc(self):
        self.level0(self.candles.stream0)
        self.level1(self.candles.stream1)
        # self.normalize(self.candles.stream1)
        self.level_base_0_8(self.candles.stream)
        self.level2(self.candles.stream2)

    def draw_stream(self, c: TCandlesList, st: TStream, stop_visible=False, colored=False, width=1):
        for si in st:
            if colored:
                drawer.fp.add_line(si.enter, si.exit, color=si.color, width=width, ax=self.ax)
            else:
                drawer.fp.add_line(si.enter, si.exit, color=cStream, width=width, ax=self.ax)
            if stop_visible:
                drawer.fp.add_line(c.dts(si.stop, -0.5), c.dts(si.stop, 0.5))

    def draw(self):
        if not self.visible: return

        self.draw_stream(self.candles, self.candles.stream, True, True, 1)
        # self.draw_stream(self.candles, self.candles.stream0, width=1)
        # self.draw_stream(self.candles, self.candles.stream1, width=2)
        # self.draw_stream(self.candles, self.candles.stream2, width=5)


class TTendencyMethod(TAnalysisMethod):
    id = 'TENDENCY'

    def acalc(self):  # asinc  -- расчитывает например сразу появление 4ки и текущую свечу
        pass

    def calc(self):
        st = self.candles.stream
        tc = self.candles.tendency

        def recurcy(ep):  # ep - even point
            i = st.index(ep.si) + 1
            if i < len(st) - 1:
                while i < len(st) - 1 and tc.between_last2p(st[i]):
                    i += 1

                if tc.begin().si.up:
                    if st[i].enter[1] > ep.si.enter[1]:
                        recurcy(tc.add2p(ep, st.find_min(ep.si, st[i]), st[i]))
                    else:
                        recurcy(tc.enlarge(ep, st[i], ep.prev))
                else:  # dn
                    if st[i].enter[1] > ep.si.enter[1]:
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
        if not self.visible: return
        tc = self.candles.tendency

        i = 0
        while i < len(tc) - 1:
            drawer.fp.add_line(tc[i].coord(), tc[i + 1].coord(), color="00FFF0", ax=self.ax)
            drawer.fp.add_text(tc[i].coord(), self.title(tc[i]), self.color(tc.begin(i - 1)),
                               ax=self.ax)  # color="eee")
            if tc[i].enlarge and i > 0:
                drawer.fp.add_line(tc[i - 1].coord(), tc[i + 1].coord(value=tc[i - 1].si.enter[1]), color="ddd",
                                   width=1, ax=self.ax)
            i += 1


class TCorrectionMethod(TAnalysisMethod):
    id = 'CORRECTION'


class TVlkFlowMethods(TFlowDonwgradeMethod):
    id = 'VLK-FLOW'  # все методы в одном, на основе Flow (Stream, Tendency, Correction)


class TVlkSystem(TAnalysisSystem):
    def __init__(self, ms: TMetaSymbol, _drawer: TDrawer):
        super().__init__(ms, _drawer)
        logger.info(">> Vlk system init")

    def add_methods(self, interval: Interval, _ax):
        # либо Vkl-Flow
        d = self.ms.future.candles.get(interval)
        self.methods.append(TInfoMethod(self.ms, d, _ax, visible=False))
        self.methods.append(TMoneyMethod(self.ms, d, _ax, visible=False))
        self.methods.append(TStreamMethod(self.ms, d, _ax, visible=True))
        self.methods.append(TTendencyMethod(self.ms, d, _ax, visible=True))

        # self.methods.append(TCorrectionMethod(self.ms))

    def main(self):
        # self.ms.spotT1.refresh()
        self.ms.future.refresh()
        super().main()

# if len(st) > 0 and st[-1].is_smothing(c[i], c[i + 1]):  # smothing убрать?
#     st.append(TStreamItem(c[i].enter, c[i+1].enter))
