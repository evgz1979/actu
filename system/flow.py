import drawer
from system.abstract import *
from system.stream import StreamMethod


class FlowMethod(StreamMethod):
    id = 'FLOW'

    def calc(self):
        self.level0(self.candles.stream0)
        self.level_base_0_8(self.candles.flow)

    def draw(self):
        # if not self.visible: return

        self.draw_stream(self.candles, self.candles.flow)









# class AbstractFlowMethod(AnalysisMethod):
#     id = 'FLOW'  # все методы в одном, на основе Flow (Stream, Tendency, Correction)
#     # stream потом взять отсюда? и остальные? то есть это абстрактый метод???
#
#
# class FlowMethod(AnalysisMethod):
#     id = 'FLOW'
#
#
# class TreeFlowMethod(AnalysisMethod):
#     id = 'TREE-FLOW'
#
#     # data: tree
#
#
# class FlowDonwgradeMethod(FlowMethod):
#     id = 'DOWNGRADEFLOW'
