from system.abstract import *
from system.flow import *
from system.info import *
from system.moneys import *
from PyQt5.uic.properties import QtCore
import drawer
from system import *
from candles import *
from system.stream import StreamMethod


class TendencyMethod(AnalysisMethod):
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


class CorrectionMethod(AnalysisMethod):
    id = 'CORRECTION'


class VolkSystem(AnalysisSystem):

    def __init__(self, m: MetaSymbol, _drawer: TDrawer):
        super().__init__(m, _drawer)
        logger.info(">> Volk system init")

    def add_methods(self, s: Symbol, candles: TCandlesList, ax):
        self.methods.append(InfoMethod(s, candles, ax, visible=False))
        self.methods.append(MoneyMethod(s, candles, ax, visible=False))
        self.methods.append(StreamMethod(s, candles, ax, visible=True))
        self.methods.append(TendencyMethod(s, candles, ax, visible=True))

    def add_interval(self, interval: Interval):  # todo -- проверять если фьючерс и нужно ли это
        c1 = self.meta.spotT0.get_candles(interval)
        c2 = self.meta.future.get_candles(interval)

        ax1 = self.drawer.add_window(self.meta.name, [self.meta.spotT0.data.day1, self.meta.future.data.day1])

        self.add_methods(self.meta.spotT0, c1, ax1[0])
        self.add_methods(self.meta.future, c2, ax1[1])

    def main(self):
        super().main()
        self.draw()

# if len(st) > 0 and st[-1].is_smothing(c[i], c[i + 1]):  # smothing убрать?
#     st.append(TStreamItem(c[i].enter, c[i+1].enter))
