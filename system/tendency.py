from system.moneys import *
import drawer
from candles import *


class TendencyMethod(AnalysisMethod):
    id = 'TENDENCY'

    def acalc(self):  # asinc  -- расчитывает например сразу появление 4ки и текущую свечу
        pass

    # def calc(self):
    #     st = self.candles.stream
    #     tc = self.candles.tendency
    #
    #     def recurcy(ep: TendencyPoint):  # ep - even point
    #         i = st.index(ep.si) + 1  # i = ep.si.index - так не работает, почему?
    #         if i < len(st) - 1:
    #             while tc.current().between_last2p(st[i]):  # todo - здесь коррекция
    #                 i += 1
    #             else:
    #                 if ep.up:
    #                     if st[i].enter[1] > ep.si.enter[1]:
    #                         recurcy(tc.current().add2p(st.find_min(ep.si, st[i]), st[i], ep.index))
    #                     else:
    #                         recurcy(tc.union(ep, st[i]))
    #                 else:  # dn
    #                     if st[i].enter[1] > ep.si.enter[1]:
    #                         recurcy(tc.union(ep, st[i]))
    #                     else:
    #                         recurcy(tc.current().add2p(st.find_max(ep.si, st[i]), st[i], ep.index))
    #
    #     recurcy(tc.start(st[0], st[1]))
    #
    #     #  --- ниже это для текущей ситуации?
    #     # if tc.current().between_last2p(tc.current()[-1].si):
    #     #     tc.current()[-1].si = tc.current()[-2].si

    # def calc(self): -- worked
    #     st = self.candles.stream
    #     tc = self.candles.tendency
    #
    #     def correction():
    #         pass
    #
    #     def recurcy(ep: FlowPoint):  # ep - even point
    #         i = st.index(ep.si) + 1  # i = ep.si.index - так не работает, почему?
    #         # print('i=', i, ', ranges=', len(tc.ranges))
    #         if i < len(st) - 1:
    #             while tc.range.between_last2p(st[i]):
    #                 correction()
    #                 i += 1
    #             else:
    #                 if ep.up:
    #                     if st[i].enter[1] > ep.si.enter[1]:
    #                         recurcy(tc.range.add2p(st.find_min(ep.si, st[i]), st[i], ep.index))
    #                         print(ep.index, 'range1=', tc.range.index)
    #                     else:
    #                         recurcy(tc.union(ep, st[i]))
    #                 else:  # dn
    #                     print('here')
    #                     if st[i].enter[1] > ep.si.enter[1]:
    #                         recurcy(tc.union(ep, st[i]))
    #                     else:
    #                         recurcy(tc.range.add2p(ep, st.find_max(ep.si, st[i]), st[i], ep.index))
    #
    #     recurcy(tc.range.start(st[0], st[1]))

    def calc(self):  # ------------------- its FLOW !!!! ----
        st = self.candles.stream
        tc = self.candles.tendency

        def recurcy(ep: FlowPoint):  # ep - even point   -------->>>>> Flow !!!
            print(ep.si.index)
            if ep.si.index > len(st): return
            i = ep.si.index+1

            while tc.range.between_last2p(st[i-1]) and i < len(st):  # correction
                i += 1

            print('i=', i, 'ep.si.index=', ep.si.index)

            # ниже условия независимо от up/dn, только на основе разницы индексов анализировать!
            if i - ep.si.index == 1:  # нечётная, объединение
                print('union')
                recurcy(tc.union(ep, st[i-1]))
            if i - ep.si.index == 2:  # чётная, след точка тенденции
                print('add2p')
                p = tc.range.add2p(st[i - 2], st[i - 1], ep.index)
                print('p', ep.si.index, p.si.index)
                recurcy(p)

        recurcy(tc.range.start(st[0], st[1]))

    def draw(self):  # todo debug-mode -- ? отображение надписей, в обыном режиме - рисовать
        # return

        # delta_ts = self.candles[1].ts - self.candles[0].ts  # todo --> Candles
        tc = self.candles.tendency

        tc._current_range_index = 1

        drawer.fp.add_text(tc.range[0].coord(), tc.range[0].title(), tc.range[0].si.color, ax=self.ax)
        i = 1
        while i < len(tc.range):
            drawer.fp.add_line(tc.range[i - 1].coord(), tc.range[i].coord(), tc.range[0].si.color, ax=self.ax, width=3)
            drawer.fp.add_text(tc.range[i].coord(), tc.range[i].title(), tc.range[0].si.color, ax=self.ax)

            if tc.range.frsi is not None:
                drawer.fp.add_line(tc.range.frsi.coord(), tc.range.frsi.coord(self.ts_delta() * 5), color=cGray,
                                   ax=self.ax, width=1)
            # print(tc.range.frsi.coord(), tc.range.frsi.coord(delta=1))
            i += 1

        tc._current_range_index = 0

    # def draw(self):  # todo debug-mode -- ? отображение надписей, в обыном режиме - рисовать
    #
    #     ri = 1
    #     for r in self.candles.tendency.ranges:
    #         if ri == 1:
    #             i = 0
    #             drawer.fp.add_text(r[i].coord(), r[i].title(), self.color(r[i]), ax=self.ax)
    #             i = 1
    #             while i < len(r):
    #                 drawer.fp.add_line(r[i-1].coord(), r[i].coord(), self.color(r[i]), ax=self.ax, width=r.range_index+1)
    #                 # if i == len(r)-1:
    #                 drawer.fp.add_text(r[i].coord(), r[i].title(), self.color(r[i]), ax=self.ax)
    #
    #                 # if r[i].enlarge and i > 0:
    #                 #     drawer.fp.add_line(r[i - 1].coord(), r[i + 1].coord(value=r[i - 1].si.enter[1]),
    #                 #                        color="ddd", width=1, ax=self.ax)
    #
    #                 i += 1
    #             # if r[i-2].enlarge:
    #             #     drawer.fp.add_line(r[i - 2].coord(), r[i].coord(value=r[i].si.enter[1]), color="ddd", width=1, ax=self.ax)
    #         ri += 1

####---------old
# st = self.candles.stream
# tc = self.candles.tendency
#
# def recurcy(ep: TTendencyPoint):  # ep - even point
#     i = st.index(ep.si) + 1
#     if i < len(st) - 1:
#         while tc.between_last2p(st[i]):  # todo - здесь коррекция
#             print(i)
#             i += 1
#         else:
#             if tc.begin().si.up:
#                 if st[i].enter[1] > ep.si.enter[1]:
#                     recurcy(tc.add2p(ep, st.find_min(ep.si, st[i]), st[i]))
#                 else:
#                     recurcy(tc.enlarge(ep, st[i]))
#             else:  # dn
#                 if st[i].enter[1] > ep.si.enter[1]:
#                     recurcy(tc.enlarge(ep, st[i]))
#                 else:
#                     recurcy(tc.add2p(ep, st.find_max(ep.si, st[i]), st[i]))
#
# recurcy(tc.start2p(st[0], st[1]))  # todo recurcy(recurcy)   --- wtf?
#
# if tc.between_last2p(tc[-1].si):
#     tc[-1].si = tc[-2].si
