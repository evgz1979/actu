from PyQt5.uic.properties import QtCore
import drawer
from system import *
from candles import *


class TInfoMethod(TAnalysisMethod):
    description = ['Candles Info Method',
                   'UpTake/PushDown candles',
                   'for _Buyer/for _Seller candles)',
                   'Limits (wick, body, close/open and for more candles)']

    def calc(self):
        # limits, so far, only 2 point
        # todo: сделать распознавание лимиток дальше чем 2 ближ свечи (позже)
        if len(self.candles) > 2:
            i = 1
            while i < len(self.candles):
                # todo проверить свечи итерирую от а=первой к последней, а когда писал код,
                # todo было чувство как в пайн-скрипт, короче проверить
                c0 = self.candles[i]
                c_1 = self.candles[i - 1]  # c_1 == c-1

                if (c0.high > c_1.high) and (c0.low < c_1.low):  # todo открытие тоже должно быть выше???
                    if c0.bullish: c0.uptake = True
                    if c0.bearish: c0.pushdown = True

                # if c0.bearish and c0.open > c_1.close and c0.close < c_1.open: c0.pushdown = True

                # todo:
                # for_buyer: False
                # for_seller: False

                if c0.high == c_1.high:
                    self.candles.limits.append(TLimit(c0, c_1, c0.high, wick=True, up=True))

                if c0.low == c_1.low:
                    self.candles.limits.append(TLimit(c0, c_1, c0.low, wick=True, dn=True))

                if c0.body_max == c_1.body_max:
                    self.candles.limits.append(TLimit(c0, c_1, c0.body_max, body=True, up=True))

                if c0.body_min == c_1.body_min:
                    self.candles.limits.append(TLimit(c0, c_1, c0.body_min, body=True, dn=True))

                if c_1.close == c0.open:
                    self.candles.limits.append(TLimit(c0, c_1, c_1.close, co=True))

                i += 1  # ! while

    def draw(self):
        pass
        # for limit in self.candles.limits:
        #     self.drawer.add_limit(limit.candle0.ts, limit.candle1.ts, limit.value)

        # for candle in self.candles:
        #     if candle.uptake:
        #         drawer.fp.plot(candle.ts, candle.low, style='o', color='#A6FFA6')
        #         # todo plot рисует по 1 точке, а нужно серией?
        #     if candle.pushdown:
        #         drawer.fp.plot(candle.ts, candle.high, style='o', color='#FFA6A6')


class TMoneyMethod(TAnalysisMethod):
    description = ['Money Method']  # todo --> descriptions.ini и все аналогичное тоже убрать (позже)

    def calc(self):
        if len(self.candles) > 2:
            i = 1
            while i < len(self.candles):
                c0 = self.candles[i]
                c1 = self.candles[i - 1]

                if (c1.bullish or c1.flat) and (c0.bullish or c0.flat) and (not (c1.flat and c0.flat)):
                    if c0.open > c1.close:
                        self.candles.moneys.append(TMoney(c0, c1, up=True, gap=True))
                    else:
                        self.candles.moneys.append(TMoney(c0, c1, up=True, maker=True))

                if (c1.bearish or c1.flat) and (c0.bearish or c0.flat) and (not (c1.flat and c0.flat)):
                    if c0.open < c1.close:
                        self.candles.moneys.append(TMoney(c0, c1, dn=True, gap=True))
                    else:
                        self.candles.moneys.append(TMoney(c0, c1, dn=True, maker=True))

                i += 1  # ! while

    def draw(self):
        pass

        # todo -- отрисовка!
        # for money in self.candles.moneys:
        #     drawer.fp.add_rect(
        #         (money.candle0.ts, money)
        #     )
        # add_limit(limit.candle0.ts, limit.candle1.ts, limit.value)


class TStreamItem:
    up: bool = False

    ts: int = 0
    value: float = 0
    index: int = 0

    stop_index: int = 0
    stop_ts: int = 0
    stop_value: float = 0

    maxmin: float = 0

    def __init__(self,
                 ts: int, value: float, index, stop_ts, stop_value, stop_index, up=False, maxmin: float = 0):
        self.ts = ts
        self.value = value
        self.index = index

        self.stop_ts = stop_ts
        self.stop_value = stop_value
        self.stop_index = stop_index

        self.up = up
        self.maxmin = maxmin

    def is_stop(self, ci, ci1: TCandle):  # c[i], c[i+1]
        if self.up:
            return ci1.low < ci.low
        else:
            return ci1.high > ci.high

    def is_duble_stop(self, ci, ci1: TCandle):  # c[i], c[i+1]
        if self.up:
            return ci1.high > ci.high
        else:
            return ci1.low < ci.low


class TStream(list[TStreamItem]):
    def get_df(self):
        df = DataFrame(columns=['ts', 'value'])
        for st in self:
            df.loc[len(df.index)] = [st.ts, st.value]
        return df

    def get_df_stop(self):
        dfs = DataFrame(columns=['ts', 'value'])
        for st in self:
            dfs.loc[len(dfs.index)] = [st.stop_ts, st.stop_value]
        return dfs

    def get_stop_value(self, ci):
        if self[-1].up:
            return ci.low
        else:
            return ci.high

    def get_stop_value_invert(self, ci):
        if self[-1].up:
            return ci.high
        else:
            return ci.low


class TStreamMethod(TAnalysisMethod):
    id = ['STREAM']

    stream: TStream  # -> ?

    def __init__(self, ms: TMetaSymbol, candles: TCandlesList):
        super().__init__(ms, candles)
        self.stream = TStream()

    def calc(self):

        c0 = self.candles[0]
        if self.candles[1].high < c0.high:
            self.stream.append(TStreamItem(
                c0.ts, c0.high, 0, c0.ts, c0.high, 0, up=False, maxmin=c0.low))
        else:
            self.stream.append(TStreamItem(
                c0.ts, c0.low, 0, c0.ts, c0.low, 0, up=True, maxmin=c0.high))

        i = 0
        while i < len(self.candles)-1:
            ci = self.candles[i]
            ci1 = self.candles[i + 1]
            st = self.stream[-1]

            if st.is_stop(ci, ci1):

                # расчет точки экстремума потока
                m = st.stop_value
                _ts = ci.ts
                j = st.stop_index
                _ii = j
                if st.up:  # up
                    while j <= i:  # + 1:
                        if self.candles[j].high > m:
                            m = self.candles[j].high
                            _ii = j
                            _ts = self.candles[j].ts
                        j += 1

                else:  # dn
                    while j <= i:  # + 1:
                        if self.candles[j].low < m:
                            m = self.candles[j].low
                            _ts = self.candles[j].ts
                            _ii = j
                        j += 1

                if self.stream[-1].up:
                    if ci1.bullish and ci1.high > ci.high:  # то добавить  сразу 2 точки потока
                        #
                        # if ci1.high > ci.high:
                        #     _ts = ci1.ts
                        #     m = ci1.high
                        #     _ii = i + 1

                        self.stream.append(TStreamItem(_ts, m, _ii, ci.ts, ci.low, i, up=False, maxmin=m))
                        self.stream.append(TStreamItem(ci1.ts, ci1.low, i+1, ci.ts, ci.high, i, up=True, maxmin=m))
                    else:
                        # _max = max(ci.high, ci1.high)
                        # if _max == ci.high: _i = i
                        # else: _i = i+1
                        # self.stream.append(TStreamItem(
                        #     self.candles[_i].ts, _max, _i, ci.ts, ci.low, i, up=False, maxmin=m))

                        if ci1.high > ci.high:
                            _ts = ci1.ts
                            m = ci1.high
                            _ii = i + 1

                        self.stream.append(TStreamItem(
                            _ts, m, _ii, ci.ts, ci.low, i, up=False, maxmin=m))
                else:  # dn
                    if ci1.bearish and ci1.low < ci.low:  # то добавить  сразу 2 точки потока
                        self.stream.append(TStreamItem(_ts, m, _ii, ci.ts, ci.high, i, up=True, maxmin=m))
                        self.stream.append(TStreamItem(ci1.ts, ci1.high, i+1, ci.ts, ci.low, i, up=False, maxmin=m))
                    else:
                        # _min = min(ci.low, ci1.low)
                        # if _min == ci.low: _i = i
                        # else: _i = i+1
                        # self.stream.append(TStreamItem(
                        #     self.candles[_i].ts, _min, _i, ci.ts, ci.high, i, up=True, maxmin=m))

                        if ci1.low < ci.low:
                            _ts = ci1.ts
                            m = ci1.low
                            _ii = i + 1

                        self.stream.append(TStreamItem(
                            _ts, m, _ii, ci.ts, ci.high, i, up=True, maxmin=m))
            i += 1

    # def calc_03(self):
    #
    #     c0 = self.candles[0]
    #     if self.candles[1].high < c0.high:
    #         self.stream.append(TStreamItem(
    #             c0.ts, c0.high, 0, c0.ts, c0.high, 0, next_ts=self.candles[1].ts, up=False, maxmin=c0.low))
    #     else:
    #         self.stream.append(TStreamItem(
    #             c0.ts, c0.low, 0, c0.ts, c0.low, 0, next_ts=self.candles[1].ts, up=True, maxmin=c0.high))
    #
    #     i = 0
    #     while i < len(self.candles)-1:
    #         ci = self.candles[i]
    #         ci1 = self.candles[i + 1]
    #
    #         if self.stream[-1].is_stop(ci, ci1):
    #
    #             # if self.stream[-1].is_duble_stop(ci, ci1): i_end = i
    #             # else: i_end = i + 1
    #
    #             # расчет точки экстремума потока
    #             if self.stream[-1].up:  # up
    #                 j = self.stream[-1].stop_index
    #                 _i = j
    #                 while j <= i:  # + 1:
    #                     if self.candles[j].high > self.stream[-1].maxmin:
    #                         self.stream[-1].maxmin = self.candles[j].high
    #                         _i = j
    #                     j += 1
    #
    #             else:  # dn
    #                 j = self.stream[-1].stop_index
    #                 _i = j
    #                 while j <= i:  # + 1:
    #                     if self.candles[j].low < self.stream[-1].maxmin:
    #                         self.stream[-1].maxmin = self.candles[j].low
    #                         _i = j
    #                     j += 1
    #
    #             _up = self.stream[-1].up
    #             _maxmin = self.stream[-1].maxmin
    #             _ts = self.candles[_i].ts
    #
    #             # уточнение точек экстремума
    #             if _up and self.candles[i + 1].high > _maxmin:
    #                 _maxmin = self.candles[i + 1].high
    #                 _ts = self.candles[i + 1].ts
    #                 _i = i + 1
    #             if not _up and self.candles[i + 1].low < _maxmin:
    #                 _maxmin = self.candles[i + 1].low
    #                 _ts = self.candles[i + 1].ts
    #                 _i = i + 1
    #
    #             self.stream.append(TStreamItem(_ts, _maxmin, _i, ci.ts, self.stream.get_stop_value(ci), i,
    #                                            next_ts=ci1.ts, up=not self.stream[-1].up, maxmin=_maxmin))
    #
    #             # проверяем вторую строну свечи
    #             # if self.stream[-1].is_stop(ci, ci1):
    #             #     stop_2 = self.stream.get_stop_value(self.candles[i])
    #             #
    #             #     self.stream.append(TStreamItem(0, 0, 0, ci.ts, self.stream.get_stop_value(ci), i,
    #             #                                    next_ts=ci1.ts, up=not self.stream[-1].up))
    #
    #         i += 1

    # def calc_01(self):
    #
    #     def stream_stop(_item: TStreamItem, _c0, _c1: TCandle):
    #         if _item.up: return _c1.low < _c0.low
    #         else: return _c1.high > _c0.high
    #
    #     # for zero point stream:
    #     c0 = self.candles[0]
    #     if self.candles[1].high < c0.high:
    #         self.stream.append(TStreamItem(c0.ts, c0.high, up=False, maxmin=c0.low))
    #         self.stream[-1].stop_value = c0.high
    #     else:
    #         self.stream.append(TStreamItem(c0.ts, c0.low, up=True, maxmin=c0.high))
    #         self.stream[-1].stop_value = c0.low
    #     self.stream[-1].stop_index = 0
    #     self.stream[-1].stop_ts = self.stream[-1].next_ts = c0.ts
    #
    #     i = 0
    #     while i < len(self.candles)-1:
    #
    #         if stream_stop(self.stream[-1], self.candles[i], self.candles[i + 1]):
    #
    #             # расчет точки остановки потока
    #             if self.stream[-1].up: stop_1 = self.candles[i].low
    #             else: stop_1 = self.candles[i].high
    #
    #             # расчет точки экстремума потока
    #             if self.stream[-1].up:  # up
    #                 j = self.stream[-1].stop_index
    #                 _i = j
    #                 while j <= i:  # + 1:  # нет! с + 1 не работает, ниже отдельно проверять
    #                     if self.candles[j].high > self.stream[-1].maxmin:
    #                         self.stream[-1].maxmin = self.candles[j].high
    #                         _i = j
    #                     j += 1
    #
    #             else:  # dn
    #                 j = self.stream[-1].stop_index
    #                 _i = j
    #                 while j <= i:  # + 1:  # нет! с + 1 не работает, ниже отдельно проверять
    #                     if self.candles[j].low < self.stream[-1].maxmin:
    #                         self.stream[-1].maxmin = self.candles[j].low
    #                         _i = j
    #                     j += 1
    #
    #             _up = self.stream[-1].up
    #             _maxmin = self.stream[-1].maxmin
    #             _ts = self.candles[_i].ts
    #
    #             # уточнение точек экстремума
    #             # todo (i+1 и внутренние!!!)  # todo -- уточнить для bullish !!!!
    #             if _up \
    #                     and self.candles[i + 1].high > _maxmin:
    #                 _maxmin = self.candles[i + 1].high
    #                 _ts = self.candles[i + 1].ts
    #                 _i = i + 1
    #             if not _up \
    #                     and self.candles[i + 1].low < _maxmin:
    #                 _maxmin = self.candles[i + 1].low
    #                 _ts = self.candles[i + 1].ts
    #                 _i = i + 1
    #
    #             # добавить точку экстремума потока
    #             item = TStreamItem(_ts,
    #                                _maxmin,
    #                                _i,
    #                                up=not self.stream[-1].up,  # направление противоположное посл точке потока
    #                                maxmin=_maxmin)
    #             self.stream.append(item)
    #
    #             # добавить точку остановки потока в запись точки экстремума потока (после нахождения экстремума !)
    #             # не перемещать этот блок выше!
    #             self.stream[-1].stop_index = i
    #             self.stream[-1].stop_ts = self.candles[i].ts
    #             self.stream[-1].stop_value = stop_1
    #             self.stream[-1].next_ts = self.candles[i + 1].ts
    #
    #             if len(self.stream) > 1 and self.stream[-1].stop_index - self.stream[-2].stop_index == 0:
    #                 # если добавились две точки остановки потока на одной свече
    #                 i += 1
    #
    #         # todo здесь хз !!!
    #         i += 1
    #         # else:
    #         #     i += 1

    def draw(self):
        if len(self.stream) > 2:
            delta_ts = self.candles[1].ts - self.candles[0].ts
            i = 0
            while i < len(self.stream) - 2:
                drawer.fp.add_line(
                    (self.stream[i].stop_ts, self.stream[i].stop_value),
                    (self.stream[i].stop_ts + delta_ts/2, self.stream[i].stop_value),
                    color="#bbb"
                )
                drawer.fp.add_line(
                    (self.stream[i].ts, self.stream[i].value),
                    (self.stream[i + 1].ts, self.stream[i + 1].value),
                    color="#B9A6FF", width=3
                )
                i += 1


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


class TTemplateMethod(TAnalysisMethod):  # (SourceTrace)
    description = ['паттерны', '']
    citation = [' ... кто-то копит "шортистов"/"лонгистов" и с их подъсъема входим...']
    interpretation = []  # объяснение метода в диалоге с пользователем
    todo = ['на основании этого метода сделать мой метод пробой']
    pass


class TVlkSystem(TAnalysisSystem):
    def __init__(self, ms: TMetaSymbol, _drawer: TDrawer):
        super().__init__(ms, _drawer)
        logger.info(">> Vlk system init")

        self.methods.append(TInfoMethod(self.ms, self.ms.spot_T0.candles.day1))
        self.methods.append(TMoneyMethod(self.ms, self.ms.spot_T0.candles.day1))
        self.methods.append(TStreamMethod(self.ms, self.ms.spot_T0.candles.day1))

        # self.methods.append(TTendencyMethod(self.ms))
        # self.methods.append(TCorrectionMethod(self.ms))

    def main(self):
        self.ms.spot_T0.refresh()
        super().main()






        # # c0    c+1 !!! -- вперед + 1 надо смотреть!!! ###
        # def stream_stop(_item: TStreamItem, _c0, _c1: TCandle):
        #     if _item.up:
        #         return _c1.low < _c0.low
        #     else:
        #         return _c1.high > _c0.high
        #
        # # for zero point stream:
        # c0 = self.candles[0]
        # if self.candles[1].high < c0.high:
        #     self.stream.append(TStreamItem(c0.ts, c0.high, up=False, maxmin=c0.low))
        #     self.stream[-1].stop_value = c0.high
        # else:
        #     self.stream.append(TStreamItem(c0.ts, c0.low, up=True, maxmin=c0.high))
        #     self.stream[-1].stop_value = c0.low
        # self.stream[-1].stop_index = 0
        # self.stream[-1].stop_ts = c0.ts
        # self.stream[-1].next_ts = c0.ts
        #
        # i = 0
        # while i < len(self.candles) - 2:
        #     print(i)
        #     if stream_stop(self.stream[-1], self.candles[i], self.candles[i + 1]):
        #         # расчет точки остановки потока
        #         if self.stream[-1].up:
        #             stop_1 = self.candles[i].low
        #         else:
        #             stop_1 = self.candles[i].high
        #
        #         print('before', i, self.stream[-1].up)
        #         # пока добавляем, потом будем уточнять
        #         # if (not ((self.candles[i].bullish and self.candles[i + 1].bullish) or
        #         #          (self.candles[i].bearish and self.candles[i + 1].bearish))) and \
        #         #         (self.stream[-1].stop_index - i > 0):
        #         self.stream.append(TStreamItem(0, 0, up=not self.stream[-1].up))
        #         print('after add', i, self.stream[-1].up)
        #
        #         self.stream[-1].stop_index = i
        #         self.stream[-1].stop_ts = self.candles[i].ts
        #         self.stream[-1].stop_value = stop_1
        #         self.stream[-1].next_ts = self.candles[i + 1].ts
        #
        #         if len(self.stream) > 1 and self.stream[-1].stop_index - self.stream[-2].stop_index == 0:
        #             # если добавились две точки остановки потока на одной свече
        #             i += 1
        #
        #     else:
        #         i += 1
        #
        #
        #
        #






        # if stream_stop(self.stream[-1], self.candles[i], self.candles[i + 1]):
        #
        #     # if i > 0: i -= 1
        #
        #     # расчет точки остановки потока
        #     if self.stream[-1].up:
        #         stop_1 = self.candles[i].low
        #     else:
        #         stop_1 = self.candles[i].high
        #
        #     # расчет точки экстремума потока
        #     if self.stream[-1].up:
        #         # j = self.stream[-1].index + 1
        #         j = _last_stop_index
        #         _i = j
        #         while j <= i:  # + 1:  # нет! с + 1 не работает, ниже отдельно проверять
        #             if self.candles[j].high > self.stream[-1].maxmin:
        #                 self.stream[-1].maxmin = self.candles[j].high
        #                 _i = j
        #             j += 1
        #
        #     else:  # dn
        #         # j = self.stream[-1].index + 1
        #         j = _last_stop_index
        #         _i = j
        #         while j <= i:  # + 1:  # нет! с + 1 не работает, ниже отдельно проверять
        #             if self.candles[j].low < self.stream[-1].maxmin:
        #                 self.stream[-1].maxmin = self.candles[j].low
        #                 _i = j
        #             j += 1
        #
        #     _up = self.stream[-1].up
        #     _maxmin = self.stream[-1].maxmin
        #     _ts = self.candles[_i].ts
        #
        #     # уточнение точек экстремума
        #     # todo (i+1 и внутренние!!!)  # todo -- уточнить для bullish !!!!
        #     if _up \
        #             and self.candles[i + 1].bearish \
        #             and self.candles[i + 1].high > _maxmin:
        #         # print(i + 1, _maxmin, self.candles[i + 1].high)
        #         _maxmin = self.candles[i + 1].high
        #         _ts = self.candles[i + 1].ts
        #         _i = i + 1
        #     if not _up \
        #             and self.candles[i + 1].bullish \
        #             and self.candles[i + 1].low < _maxmin:
        #         # print(i + 1, _maxmin, self.candles[i + 1].low)
        #         _maxmin = self.candles[i + 1].low
        #         _ts = self.candles[i + 1].ts
        #         _i = i + 1
        #
        #     # добавить точку экстремума потока
        #     item = TStreamItem(_ts,
        #                        _maxmin,
        #                        _i,
        #                        up=not self.stream[-1].up,  # направление противоположное посл точке потока
        #                        maxmin=_maxmin)
        #     self.stream.append(item)
        #
        #     # добавить точку остановки потока в запись точки экстремума потока (после нахождения экстремума !)
        #     # не перемещать этот блок выше!
        #     self.stream[-1].stop_index = i
        #     self.stream[-1].stop_ts = self.candles[i].ts
        #     self.stream[-1].stop_value = stop_1
        #     _last_stop_index = i
        #
        # i += 1

        # while i < 30:  # len(self.candles) - 1:
        #
        #     if stream_stop(self.stream[-1], self.candles[i], self.candles[i + 1]):
        #         print(i)
        #         self.stream.append(
        #             TStreamItem(self.candles[self.stream[-1].index],
        #                         self.stream[-1].maxmin,
        #                         self.stream[-1].index,
        #                         up=not self.stream[-1].up))  # направление противоположное посл точке потока
        #     else:
        #         if self.stream[-1].up:
        #             # self.stream[-1].maxmin = max(self.stream[-1].maxmin, self.candles[i].high)  # нихуя!
        #             if self.candles[i].high > self.stream[-1].maxmin:
        #                 self.stream[-1].maxmin = self.candles[i].high
        #                 self.stream[-1].index = i
        #         else:
        #             if self.candles[i].low < self.stream[-1].maxmin:
        #                 self.stream[-1].maxmin = self.candles[i].low
        #                 self.stream[-1].index = i
        #     i += 1

# if self.stream[-1].up:
#     maxmin = max(maxmin, self.candles[i].high)
#     if maxmin != self.candles[i].high: _i = i
# else:
#     maxmin = min(maxmin, self.candles[i].low)
#     if maxmin != self.candles[i].low: _i = i


# ts = self.candles[i].ts
# if self.stream[-1].up:
#     if self.candles[i + 1].high > self.candles[i].high:
#         ts = self.candles[i + 1].ts
#         maxmin = max(maxmin, self.candles[i].high)
#         i += 1
#     else:
#         ts = self.candles[i].ts
# else:
#     if self.candles[i + 1].low < self.candles[i].low:
#         ts = self.candles[i + 1].ts
#         maxmin = min(maxmin, self.candles[i].low)
#         i += 1
#     else:
#         ts = self.candles[i].ts
# дополнительно проверяем i+1 свечу  todo -- проверять серию внутренних свечей
# if self.stream[-1].up and self.candles[i+1].bearish \
#         and self.candles[i + 1].high > self.stream[-1].maxmin:
#     self.stream[-1].maxmin = self.candles[i + 1].high
#     _i = i+1

# if not self.stream[-1].up and self.candles[i+1].bullish \
#         and self.candles[i + 1].low < self.stream[-1].maxmin:
#     self.stream[-1].maxmin = self.candles[i + 1].low
#     _i = i+1
