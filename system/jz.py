# поструктуре смотреть пробитие, возврат и назад пробивает или нет, то есть создаются или нет подд/сопр

from symbols import *
from system import *

from system.abstract import *
from system.flow import *
from system.info import *


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


class TOpenInterest:
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
