from system.abstract import *
from system.flow import FlowMethod
from system.volk import TendencyMethod


class JZSystem(AnalysisSystem):
    def __init__(self, m: MetaSymbol, _drawer: TDrawer):
        super().__init__(m, _drawer)
        logger.info(">> JZ system init")

    def add_methods(self, s: Symbol, candles: TCandlesList, ax):
        self.methods.append(FlowMethod(s, candles, ax, visible=False))
        # self.methods.append(TendencyMethod(s, candles, ax, visible=True))

    def add_symbol(self, s: Symbol, interval: Interval):
        self.add_methods(s, s.get_candles(interval),
                         self.drawer.add_window(
                             Interval.get_title(interval) + ', ' + s.get_title() + ': ' + '[МЕТА: ' + self.meta.name + ']',
                             [s.data.get(interval)]))

    def add_interval(self, interval: Interval):
        self.add_symbol(self.meta.spotT0, interval)
        self.add_symbol(self.meta.future, interval)

    def main(self):
        super().main()
        self.draw()

# class TJZMethod(AnalysisMethod):
#     pass
#
#
# class TSourceTraceMethod(TJZMethod):
#     pass
#
#
# class TLevelsMethod(TJZMethod):
#     description = ['объемные и пустотные уровни', 'отмены, пробитимя, возвраты и тд, защита']
#
#
# class TSupportResistanceMethod(TJZMethod):
#     pass
#
#
# class TPriceStructureMethod(TJZMethod):
#     pass
#
#
# class TProfileVolumeStructureMethod(TJZMethod):
#     pass
#
#
# class TOpenInterest:
#     pass
#
#
# class TBalanceRelationsMethod(TJZMethod):
#     pass
#
#
# class TPushinThroughMethod(TJZMethod):
#     description = ['метод пробития/продавливания объема', 'и отслеживания возврата',
#                    'определение границ по ранним уровням или пустотным уровням'
#                    'нахождение в импульсе или импульс закончен. относителльно более верхних "ТФ"'
#                    'удерживание внутри или прокол границы']
#     pass
#
#
# class TBreakingThroughMethod(TPushinThroughMethod):  # пробитие в обратную сторону
#     pass
