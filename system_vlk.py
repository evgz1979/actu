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
        for limit in self.candles.limits:
            self.drawer.add_limit(limit.candle0.ts, limit.candle1.ts, limit.value)

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
    ts: int
    value: float
    up: bool  # not up = dn

    stop_index: int
    stop_ts: int
    stop_value: float

    index: int  # for calc
    maxmin: float  # for next item

    def __init__(self, ts: int, value: float, index=0, up=False, maxmin: float = 0):
        self.ts = ts
        self.value = value
        self.up = up
        self.index = index
        self.maxmin = maxmin

        self.stop_index = 0
        self.stop_ts = 0
        self.stop_value = value


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


class TStreamMethod(TAnalysisMethod):
    description = ['Stream Method']

    stream: TStream

    def __init__(self, ms: TMetaSymbol, candles: TCandlesList):
        super().__init__(ms, candles)
        self.stream = TStream()

    def calc(self):  # c0    c+1 !!! -- вперед + 1 надо смотреть!!! ###
        def stream_stop(item: TStreamItem, _c0, _c1: TCandle):
            if item.up:
                return _c1.low < _c0.low
            else:
                return _c1.high > _c0.high

        # for zero point stream:
        c0 = self.candles[0]
        if self.candles[1].high < c0.high:
            self.stream.append(TStreamItem(c0.ts, c0.high, up=False, maxmin=c0.low))
        else:
            self.stream.append(TStreamItem(c0.ts, c0.low, up=True, maxmin=c0.high))

        i = 0
        while i < len(self.candles) - 1:

            if stream_stop(self.stream[-1], self.candles[i], self.candles[i + 1]):

                # расчет точки остановки потока
                if self.stream[-1].up:
                    stop_1 = self.candles[i].low
                else:
                    stop_1 = self.candles[i].high

                # расчет точки экстремума потока
                j = self.stream[-1].index + 1
                _i = j
                while j <= i:  # + 1:  # нет! с + 1 не работает, ниже отдельно проверять
                    if self.stream[-1].up:
                        if self.candles[j].high > self.stream[-1].maxmin:
                            self.stream[-1].maxmin = self.candles[j].high
                            _i = j
                    else:
                        if self.candles[j].low < self.stream[-1].maxmin:
                            self.stream[-1].maxmin = self.candles[j].low
                            _i = j
                    j += 1

                # дополнительно проверяем i+1 свечу  todo -- проверять серию внутренних свечей
                # if self.stream[-1].up and self.candles[i+1].bearish \
                #         and self.candles[i + 1].high > self.stream[-1].maxmin:
                #     self.stream[-1].maxmin = self.candles[i + 1].high
                #     _i = i+1

                # if not self.stream[-1].up and self.candles[i+1].bullish \
                #         and self.candles[i + 1].low < self.stream[-1].maxmin:
                #     self.stream[-1].maxmin = self.candles[i + 1].low
                #     _i = i+1

                _up = self.stream[-1].up
                _maxmin = self.stream[-1].maxmin
                _ts = self.candles[_i].ts

                # уточнение точек экстремума
                # todo (i+1 и внутренние!!!)
                if _up and self.candles[i + 1].bearish and self.candles[i + 1].high > _maxmin:
                    print(i + 1, _maxmin, self.candles[i + 1].high)
                    _maxmin = self.candles[i + 1].high
                    _ts = self.candles[i + 1].ts
                    _i = i + 1
                # if not _up and self.candles[i + 1].bullish and self.candles[i + 1].low < _maxmin:
                #     print(i + 1, _maxmin, self.candles[i + 1].low)
                #     _maxmin = self.candles[i + 1].low
                #     _ts = self.candles[i + 1].ts
                #     _i = i + 1

                # добавить точку экстремума потока
                item = TStreamItem(_ts,
                                   _maxmin,
                                   _i,
                                   up=not self.stream[-1].up,  # направление противоположное посл точке потока
                                   maxmin=_maxmin)
                self.stream.append(item)

                # item = TStreamItem(self.candles[_i].ts,
                #                    self.stream[-1].maxmin,
                #                    _i,
                #                    up=not self.stream[-1].up,  # направление противоположное посл точке потока
                #                    maxmin=self.stream[-1].maxmin)
                # self.stream.append(item)

                # добавить точку остановки потока в запись точки экстремума потока (после нахождения экстремума !)
                # не перемещать этот блок выше!
                self.stream[-1].stop_index = i
                self.stream[-1].stop_ts = self.candles[i].ts
                self.stream[-1].stop_value = stop_1



                #     _i = i+1

            i += 1

    def draw(self):
        df = self.stream.get_df()
        dfs = self.stream.get_df_stop()
        # df.reset_index(drop=True)
        # print(df)
        drawer.fp.plot(df['ts'], df['value'], style='o')
        drawer.fp.plot(dfs['ts'], dfs['value'], style='>')

        i = 0
        while i < len(self.stream)-1:
            drawer.fp.add_line(
                (self.stream[i].ts, self.stream[i].value),
                (self.stream[i+1].ts, self.stream[i+1].value),
                color="#B9A6FF"
            )
            if self.stream[i].up: s = 'ˆ'
            else: s = 'v'
            drawer.fp.add_text((self.stream[i].ts, self.stream[i].value), s=s)
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
