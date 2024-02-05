from system import *
from system_base import *
from candles import *


class TVolkMethod(TAnalysisMethod):
    pass

#
# class TSignOfMoneyMethod(TVolkMethod):
#     gap_or_no = []
#
#     def main(self):
#         logger.info(">> Volk system -- SignOfMoney Method start")
#
#
# class TSellerBueyrMethod(TVolkMethod):
#     pass
#
#
# class TStreamMethod(TVolkMethod):
#
#     def main(self):
#         logger.info(">> Volk system -- Stream Method start")
#
#
# class TOpenForMethod(TVolkMethod):
#     description = ['открытие под продавца/покупателя']
#     pass
#
#
# class TTendencyMethod(TVolkMethod):
#
#     def main(self):
#         logger.info(">> Volk system -- Tendency Method start")
#
#
# class TCorrectionMethod(TVolkMethod):
#
#     def main(self):
#         logger.info(">> Volk system -- Correction Method start")
#
#
# class TTimeFramesRelationsMethod(TVolkMethod):
#     pass


class TTemplateMethod(TVolkMethod):  # (SourceTrace)
    description = ['паттерны', '']
    citation = [' ... кто-то копит "шортистов"/"лонгистов" и с их подъсъема входим...']
    interpretation = []  # объяснение метода в диалоге с пользователем
    todo = ['на основании этого метода сделать мой метод пробой']
    pass


class TVolkSystem(TAnalysisSystem):
    method_info: TCandlesInfoMethod

    def __init__(self, ms: TMetaSymbol, _drawer: TDrawer):
        super().__init__(ms, _drawer)
        logger.info(">> Volk system init")

        self.method_info = TCandlesInfoMethod(self.ms)
        self.methods.append(self.method_info)

        # self.methods.append(TSignOfMoneyMethod(self.ms))
        # self.methods.append(TStreamMethod(self.ms))
        # self.methods.append(TTendencyMethod(self.ms))
        # self.methods.append(TCorrectionMethod(self.ms))

    def main(self):
        self.ms.spot_T0.refresh()
        self.method_info.candles = self.ms.spot_T0.candles.day1

        super().main()
