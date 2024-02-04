from system import *
from system_base import *
from candles import *


class TVolkMethod(TAnalysisMethod):
    pass


class TSignOfMoneyMethod(TVolkMethod):
    gap_or_no = []

    def main(self):
        logger.info(">> Volk system -- SignOfMoney Method start")


class TSellerBueyrMethod(TVolkMethod):
    pass


class TStreamMethod(TVolkMethod):

    def main(self):
        logger.info(">> Volk system -- Stream Method start")


class TTendencyMethod(TVolkMethod):

    def calc(self, candles: TCandleData):
        pass

    def main(self):
        logger.info(">> Volk system -- Tendency Method start")


class TCorrectionMethod(TVolkMethod):

    def main(self):
        logger.info(">> Volk system -- Correction Method start")


class TTimeFramesRelationsMethod(TVolkMethod):
    pass


class TTemplateMethod(TVolkMethod):  # (SourceTrace)
    description = ['паттерны', '']
    citation = [' ... кто-то копит "шортистов"/"лонгистов" и с их подъсъема входим...']
    interpretation = []  # объяснение метода в диалоге с пользователем
    todo = ['на основании этого метода сделать мой метод пробой']
    pass


class TVolkSystem(TAnalysisSystem):
    def __init__(self, ms: TMetaSymbol):
        super().__init__(ms)
        logger.info(">> Volk system init")

        self.methods.append(TCandlesInfoMethod(self.ms))
        self.methods.append(TSignOfMoneyMethod(self.ms))
        self.methods.append(TStreamMethod(self.ms))
        self.methods.append(TTendencyMethod(self.ms))
        self.methods.append(TCorrectionMethod(self.ms))

