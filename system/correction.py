import drawer
from system.abstract import AnalysisMethod


class CorrectionMethod(AnalysisMethod):
    id = 'CORRECTION'

    def calc(self):
        st = self.candles.streams
        tc = self.candles.tendency
        cr = self.candles.correction

        # def recurcy(ep):  # ep - even point
        #     i = st.index(ep.si) + 1
        #     if i < len(st) - 1:
        #         while i < len(st) - 1 and tc.between_last2p(st[i]):
        #             i += 1
        #
        #         if tc.begin().si.up:
        #             if st[i].enter[1] > ep.si.enter[1]:
        #                 recurcy(tc.add2p(ep, st.find_min(ep.si, st[i]), st[i]))
        #             else:
        #                 recurcy(tc.enlarge(ep, st[i], ep.prev))
        #         else:  # dn
        #             if st[i].enter[1] > ep.si.enter[1]:
        #                 recurcy(tc.enlarge(ep, st[i], ep.prev))
        #             else:
        #                 recurcy(tc.add2p(ep, st.find_max(ep.si, st[i]), st[i]))
        #
        # recurcy(cr.start2p(st[0], st[1]))

        cr.start2p(st[0], st[1])

    def draw(self):
        cr = self.candles.correction

        i = 0
        while i < len(cr) - 1:
            drawer.fp.add_line(cr[i].coord(), cr[i + 1].coord(), color="00FFF0", ax=self.ax, width=2)
            i += 1
