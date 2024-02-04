from symbols import *
from system import *


class TJZMethod(TAnalysisMethod):
    pass


class TSourceTraceMethod(TJZMethod):
    pass


class TLevelsMethod(TJZMethod):
    description = ['объемные и пустотные уровни', 'отмены, пробитимя, возвраты и тд, защита']


class TSupportResistanceMethod(TJZMethod):
    pass


class TPriceStructureMethod(TJZMethod):
    pass


class TProfileVolumeStructureMethod(TJZMethod):
    pass


class TBalanceRelationsMethod(TJZMethod):
    pass


class TPushinThroughMethod(TJZMethod):
    description = ['метод пробития/продавливания объема', 'и отслеживания возврата',
                   'определение границ по ранним уровням или пустотным уровням'
                   'нахождение в импульсе или импульс закончен. относителльно более верхних "ТФ"'
                   'удерживание внутри или прокол границы']
    pass


class TBreakingThroughMethod(TPushinThroughMethod):  # пробитие в обратную сторону
    pass


class TJZSystem(TAnalysisSystem):
    pass
