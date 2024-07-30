import drawer
from system.abstract import *
from system.stream import StreamMethod

# TreeFlowMethod -- строит дерево, на основе потока, из которого потом строить тенденцию и коррекцию
# StructTreeFlowMethod -- а делее уточнять структуру по выходам из блоков и глобальным уровням
# ProfileStructTreeFlowMethod -- и уточнять по профилю объема это еще позже
# MetaFlow -- в итоге объединить все просто в Flow


class TreeFlowMethod(StreamMethod):
    pass
    # id = 'TREE-FLOW'
    #
    # def calc(self):
    #     # calculate stream from parent method
    #     self.level_base_0_9(self.candles.stream)
    #
    #     st = self.candles.stream
    #     tc = self.candles.tendency  # временно
    #     fl = self.candles.flow
    #
    #     def recurcy(ep: TTendencyPoint):  # ep - even point
    #         i = st.index(ep.si) + 1
    #         if i < len(st) - 1:
    #             while tc.between_last2p(st[i]):  # todo - здесь коррекция
    #                 print(i)
    #                 i += 1
    #             else:
    #                 if tc.begin().si.up:
    #                     if st[i].enter[1] > ep.si.enter[1]:
    #                         recurcy(tc.add2p(ep, st.find_min(ep.si, st[i]), st[i]))
    #                     else:
    #                         recurcy(tc.enlarge(ep, st[i]))
    #                 else:  # dn
    #                     if st[i].enter[1] > ep.si.enter[1]:
    #                         recurcy(tc.enlarge(ep, st[i]))
    #                     else:
    #                         recurcy(tc.add2p(ep, st.find_max(ep.si, st[i]), st[i]))
    #
    #     recurcy(tc.start2p(st[0], st[1]))   # todo recurcy(recurcy)   --- wtf?
    #
    #     if tc.between_last2p(tc[-1].si):
    #         tc[-1].si = tc[-2].si
    #
    # @staticmethod
    # def color(p: TTendencyPoint):  # todo --> TTendencyPoint ???как если None???
    #     if p is None: return "eee"
    #     else: return "59B359" if p.si.up else "D96C6C"
    #
    # def draw(self):
    #     self.draw_stream(self.candles, self.candles.stream, stop_visible=True, colored=True, width=2)  # for debug
    #
    #     tc = self.candles.tendency
    #
    #     i = 0
    #     while i < len(tc) - 1:
    #         drawer.fp.add_line(tc[i].coord(), tc[i + 1].coord(), color="00FFF0", ax=self.ax, width=2)
    #
    #         if tc[i].enlarge and i > 0:
    #             drawer.fp.add_line(
    #                 tc[i - 1].coord(), tc[i + 1].coord(value=tc[i - 1].si.enter[1]), color="ddd", width=1, ax=self.ax)
    #         i += 1


class MetaFlowMethod(TreeFlowMethod):
    pass







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
