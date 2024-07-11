from system.abstract import *
from system.flow import *
from system.info import *
from system.moneys import *
from PyQt5.uic.properties import QtCore
import drawer
from system import *
from candles import *
from system.stream import StreamMethod


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
        c1 = self.meta.spotT0.load_candles(interval)
        c2 = self.meta.future.load_candles(interval)

        ax1 = self.drawer.add_window(self.meta.name, [self.meta.spotT0.data.day1, self.meta.future.data.day1])

        self.add_methods(self.meta.spotT0, c1, ax1[0])
        self.add_methods(self.meta.future, c2, ax1[1])

    def main(self):
        super().main()
        self.draw()

# if len(st) > 0 and st[-1].is_smothing(c[i], c[i + 1]):  # smothing убрать?
#     st.append(TStreamItem(c[i].enter, c[i+1].enter))
