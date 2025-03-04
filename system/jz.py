from system.abstract import *
from system.stream import StreamMethod
# from system.tendency import TendencyMethod
from system.flow import FlowMethod

# Structured
# Volumed
# Candles(структура основанная на свечах)


class JZSystem(AnalysisSystem):
    def __init__(self, _drawer: TDrawer):
        super().__init__(_drawer)
        logger.info(">> JZ system init")

    def add_methods(self, interval: Interval, s: Symbol, candles: Candles, ax):
        # if interval != Interval.min5: self.methods.append(InfoMethod(s, candles, ax, visible=True))
        # if interval != Interval.min5: self.methods.append(MoneyMethod(s, candles, ax, visible=True))

        self.methods.append(StreamMethod(s, candles, ax, visible=True))
        self.methods.append(FlowMethod(s, candles, ax, visible=False))
        # self.methods.append(TendencyMethod(s, candles, ax, visible=True))
        # self.methods.append(CorrectionMethod(s, candles, ax, visible=True))

    def add_symbol(self, meta: MetaSymbol, s: Symbol, interval: Interval):
        self.add_methods(interval, s, s.load_candles(interval),
                         self.drawer.add_window(
                             Interval.get_title(interval) + ', ' + s.get_title() + ': ' + '[МЕТА: ' + meta.name + ']',
                             [s.data.get(interval)], maximize=True))

    def add_interval(self, meta: MetaSymbol, interval: Interval):
        self.add_symbol(meta, meta.spotT0, interval)
        # self.add_symbol(meta, meta.future, interval)

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
