from system.moneys import *
import drawer
from temp.candles import *


class FlowMethod(AnalysisMethod):
    id = 'Flow'

    def acalc(self):  # asinc  -- расчитывает например сразу появление 4ки и текущую свечу
        pass

    def calc(self):

        self.candles.flow.calc()

        print('-------ranges=', len(self.candles.flow.ranges))

    def draw(self):  # todo debug-mode -- ? отображение надписей, в обыном режиме - рисовать

        tc = self.candles.flow

        tc.debug_current_index = 1

        # drawer.fp.add_text(tc.range[0].coord(), tc.range[0].title(), tc.range[0].si.color, ax=self.ax)

        i = 1

        while i < len(tc.range):
            drawer.fp.add_line(tc.range[i - 1].coord(), tc.range[i].coord(), tc.range[i-1].color, ax=self.ax, width=3)
            if i == len(tc.range) - 1: s1 = ' (range=' + str(tc.debug_current_index) + ')'
            else: s1 = ''
            s2 = ', up='+str(tc.range[i].up) + ' ,enl=' + str(tc.range[i].enlarge)
            # drawer.fp.add_text(tc.range[i].coord(), tc.range[i].title() + s1 + s2, tc.range[i].color, ax=self.ax)

            if tc.range.frsi is not None:
                drawer.fp.add_line(tc.range.frsi.coord(), tc.range.frsi.coord(self.ts_delta() * 5), color=cGray,
                                   ax=self.ax, width=2)
            # print(tc.range.frsi.coord(), tc.range.frsi.coord(delta=1))
            i += 1

        tc.debug_current_index = 0
