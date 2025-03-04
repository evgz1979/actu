import drawer
from system.abstract import AnalysisMethod
from base.candles import *


class StreamMethod(AnalysisMethod):
    id = 'STREAM'

    def calc(self):
        self.candles.streams.calc(self.skip_i())

    def draw_stream(self, st: SimpleStream, stop_visible=False, colored=False, width=1):
        for si in st:
            if colored:
                drawer.fp.add_line(si.enter, si.exit, color=si.color, width=width, ax=self.ax)
            else:
                drawer.fp.add_line(si.enter, si.exit, color=cStream, width=width, ax=self.ax)

            # if stop_visible:  # --- ------ возникает ошибка отрисовки, почему?
            #     drawer.fp.add_line(c.dts(si.stop, -0.5), c.dts(si.stop, 0.5))

    def draw(self):
        self.draw_stream(self.candles.streams.base, True, True, 1)
        # self.draw_stream(self.candles.stream0, True, True, 1)
        # self.draw_stream(self.candles.stream1, True, True, 1)



# -------------------
#
# class StreamMethod(AnalysisMethod):
#     id = 'STREAM'
#
#
#
#     def calc(self):
#
#         # self.level0(self.candles.stream0)
#         # self.level1(self.candles.stream1)
#         # self.normalize(self.candles.stream1)
#
#         self.candles.calc_stream(self.candles.stream, self.skip_i())
#
#         # self.level2(self.candles.stream2)
#
#     def draw_stream(self, st: Stream, stop_visible=False, colored=False, width=1):
#         for si in st:
#             if colored:
#                 drawer.fp.add_line(si.enter, si.exit, color=si.color, width=width, ax=self.ax)
#             else:
#                 drawer.fp.add_line(si.enter, si.exit, color=cStream, width=width, ax=self.ax)
#
#             # if stop_visible:  # --- ------ возникает ошибка отрисовки, почему?
#             #     drawer.fp.add_line(c.dts(si.stop, -0.5), c.dts(si.stop, 0.5))
#
#     def draw(self):
#         self.draw_stream(self.candles.stream, True, True, 1)
#         # self.draw_stream(self.candles, self.candles.stream0, width=1)
#         # self.draw_stream(self.candles, self.candles.stream1, width=2)
#         # self.draw_stream(self.candles, self.candles.stream2, width=5)

    # def level_base_0_7(self, st: TStream):  # ver 0.7
    #     c = self.candles
    #     st.append(TStreamItem(c[0].enter, c[0].exit, c[0].enter))
    #
    #     p = False  # pass
    #     i = 0
    #     while i < len(c) - 1:
    #
    #         if st[-1].is_stop2(c[i], c[i + 1]):
    #
    #             ex = st[-1].get_exit(c[i + 1])
    #
    #             if st[-1].up:
    #                 if c[i + 1].high > st[-1].exit[1]:
    #                     if c[i + 1].bearish:
    #                         st[-1].exit = c[i + 1].enter
    #
    #                     else:  # c[i+1].bullish:
    #                         st.append(TStreamItem(st[-1].exit, c[i + 1].enter))
    #                         st.append(TStreamItem(c[i + 1].enter, c[i + 1].exit))
    #                         ex = c[i + 1].exit
    #                 else:  # c[i+1].high <= st[-1].exit[1]:   # todo error !!! on candle 2024-01-04
    #                     if c[i + 1].bearish and st[-1].exit[0] < c[i].ts:
    #                         st.append(TStreamItem(st[-1].exit, c[i].enter))
    #                         st.append(TStreamItem(c[i].enter, c[i + 1].enter))
    #                         ex = c[i + 1].exit
    #                     # else:
    #                     #     p = True
    #
    #             else:  # dn
    #                 if c[i + 1].low < st[-1].exit[1]:
    #                     if c[i + 1].bullish:
    #                         st[-1].exit = c[i + 1].enter
    #
    #                     # else:   # c[i + 1].bearish
    #
    #             # if st[-1].exit[1] == ex[1]:
    #             #     pass
    #             # else:
    #
    #             # if p:
    #             #     p = False
    #             # else:
    #             st.append(TStreamItem(st[-1].exit, ex, st[-1].get_stop(c[i])))
    #
    #         else:
    #             st[-1].move_exit(c[i], c[i + 1])
    #
    #         i += 1
    #
    #         # self.candles.stream.normalize()  todo ???

    # def level_base_0_8(self, st: TStream):  # ver 0.8
    #     c = self.candles
    #     # ign = self.symbol.info.ignore_candles_count  # =0 -- пока не использую ign
    #
    #     # todo -- if ign > 0: ???? перенести ??? неправильно считает?
    #     # print('ign candle dt', c[ign].dt, c[ign].high)
    #     # print('ign candle enter', c[ign].enter, datetime.fromtimestamp(c[ign].enter[0]))
    #     # print('symbol.info.ignore_candles_count', ign)
    #
    #     i = self.skip_i()
    #     st.append(TStreamItem(c[i].enter, c[i].exit, c[i].enter))
    #
    #     while i < len(c) - 1:
    #         ex = st[-1].move_exit(c[i], c[i + 1])
    #
    #         if st[-1].is_stop2(c[i], c[i + 1]):
    #             st.append(TStreamItem(st[-1].exit, ex, st[-1].get_stop(c[i])))
    #
    #         i += 1

    # def level_base_0_9(self, st: Stream):  # ver 0.8
    #     c = self.candles
    #     i = self.skip_i()
    #     st.append(StreamItem(c[i].enter, c[i].exit, c[i].enter, index=i - self.skip_i() + 1))
    #
    #     while i < len(c) - 1:
    #         ex = st[-1].move_exit(c[i], c[i + 1])  # переносим выход, пока ...
    #
    #         if st[-1].is_stop2(c[i], c[i + 1]):  # переносим выход, пока ...
    #             st.append(StreamItem(st[-1].exit, ex, st[-1].get_stop(c[i]),
    #                                  index=i - self.skip_i() + 1))
    #         i += 1


###===-----  worked!!!

    # @staticmethod
    # def is_correction(ci, ci1: TCandle):
    #     return (ci.enter[1] <= ci1.low <= ci.exit[1] < ci1.high) or (
    #             ci.enter[1] >= ci1.high >= ci.exit[1] > ci1.low)

    # def level0(self, st: Stream):
    #     c = self.candles
    #     i = 0
    #     while i < len(c) - 1:
    #         st.append(StreamItem(c[i].enter, c[i].exit, visible=False))
    #         st.append(StreamItem(c[i].exit, c[i + 1].enter, visible=False))
    #         i += 1
    #
    # def level1(self, st: Stream):
    #     c = self.candles
    #     i = 0
    #     while i < len(c) - 1:
    #         if len(st) > 0 and self.is_correction(c[i], c[i + 1]):
    #             st.append(StreamItem(c[i].enter, c[i + 1].enter, visible=False))
    #         # elif len(st) > 0 and self.is_merge_wicks(c[i], c[i + 1]):
    #         else:
    #             # level0(st)
    #             st.append(StreamItem(c[i].enter, c[i].exit, visible=False))
    #             st.append(StreamItem(c[i].exit, c[i + 1].enter, visible=False))
    #         i += 1
    #
    # def level_base_0_91(self, st: Stream):
    #     c = self.candles
    #     i = self.skip_i()
    #     st.append(StreamItem(c[i].enter, c[i].exit, c[i].enter, candle_index=i - self.skip_i(), index=1))
    #
    #     while i < len(c) - 1:
    #         ex = st[-1].move_exit(c[i], c[i + 1])  # переносим выход, пока ...
    #
    #         if st[-1].is_stop2(c[i], c[i + 1]):
    #             st.append(StreamItem(st[-1].exit, ex, st[-1].get_stop(c[i]), candle_index=i - self.skip_i(),
    #                                  index=len(st)+1))
    #         i += 1
    #
    # def level2(self, st: Stream):
    #     c = self.candles
    #     st1 = self.candles.stream1
    #     st.append(StreamItem(st1[0].enter, st1[0].enter, st1[0].enter))
    #
    #     i = 0
    #     while i < len(c) - 1:
    #         # if st[-1].is_stop2(c[i], c[i + 1]):
    #         #     st.append(TStreamItem(
    #         #         st[-1].exit,
    #         #         st1.get_exit(st[-1], c[i], c[i + 1]),
    #         #         st[-1].get_stop(c[i])))
    #         i += 1