import finplot as fp
from pandas import DataFrame


class TDrawer:
    ax = {}

    def __init__(self):
        fp.candle_bull_color = '#6c9'
        fp.candle_bull_body_color = '#6c9'

    def append(self, name, df: DataFrame):
        self.ax[name] = fp.candlestick_ochl(df[['open', 'close', 'high', 'low']])

    @staticmethod
    def add_limit(ts0, ts1, value):
        fp.add_line((ts0, value), (ts1, value), color='#FF00FF', width=2)

    @staticmethod
    def show():
        fp.show()



#
# def draw2(df: DataFrame):
#     fp.background = '#cfc'
#     fp.candle_bull_color = '#6c9'
#     fp.candle_bear_color = '#336'
#     fp.candle_bull_body_color = '#6c9'
#     fp.candlestick_ochl(df[['open', 'close', 'high', 'low']])
#
#     # --- расчеты потом убрать из drawer -- в отд модуль
#     dt1 = []
#     stream1 = []
#
#     def add_s(_ts1, _stream1):
#         dt1.append(_ts1)
#         stream1.append(_stream1)
#
#     def bullish(r):
#         return r.open < r.close
#
#     def inside_candle(c1, c2):
#         return c2.high <= c1.high and c2.low >= c1.low
#
#     # --- gap or no & limits---   пока только есди лимитные деньги --- короче все расписать тут
#     candle_prev = None
#     _ts = None
#     for ts, candle in df.iterrows():
#         if candle_prev is not None:
#             if candle_prev.close == candle.open:  # limits and candles gaps
#                 fp.add_rect((_ts, candle_prev.close - 30), (ts, candle.open + 30))
#
#             # -- dn or up candle
#             if candle.high <= candle_prev.high: df.at[ts, 'dn'] = 1
#             if candle.low >= candle_prev.low: df.at[ts, 'up'] = 1
#         candle_prev = candle
#         _ts = ts
#
#     fp.show()
#
#
# def draw1(df: DataFrame):
#     fp.background = '#cfc'
#     fp.candle_bull_color = '#6c9'
#     fp.candle_bear_color = '#336'
#     fp.candle_bull_body_color = '#6c9'
#     fp.candlestick_ochl(df[['open', 'close', 'high', 'low']])
#
#     # пробую рисовать потоки
#     # --- расчеты потом убрать из drawer
#     dt1 = []
#     stream1 = []
#
#     def add_s(_ts1, _stream1):
#         dt1.append(_ts1)
#         stream1.append(_stream1)
#
#     def bullish(r):
#         return r.open < r.close
#
#     def inside_candle(c1, c2):
#         return c2.high <= c1.high and c2.low >= c1.low
#
#     _candle = None
#     _ts = None
#     for ts, candle in df.iterrows():
#         if _candle is not None:
#             if _candle.close == candle.open:  # limits and candles gaps
#                 fp.add_rect((_ts, _candle.close - 30), (ts, candle.open + 30))
#             if candle.high <= _candle.high: df.at[ts, 'dn'] = 1
#             if candle.low >= _candle.low: df.at[ts, 'up'] = 1
#         _candle = candle
#         _ts = ts
#
#     # ----------------------------
#     add_s(df.index[0], _candle.low if bullish(_candle) else _candle.high)
#     i = 1
#     _candle = df.iloc[0]
#     candle = df.iloc[1]
#     while i < df.shape[0] - 1:
#         _candle = df.iloc[i-1]
#         candle = df.iloc[i]
#         _i = i
#         if inside_candle(_candle, candle):
#             while inside_candle(_candle, candle):
#                 i = i + 1
#                 candle = df.iloc[i]
#                 # print('inside', i-1)
#         elif candle.high <= _candle.high:
#             while candle.high <= _candle.high:
#                 _candle = candle
#                 candle = df.iloc[i]
#                 i = i + 1
#             if i > _i:
#                 # print('dn stop', i-1-1)
#                 _i_stop = i-1-1  # -1 тк от нуля, и еще -1 тк предыдущая
#                 _candle = df.iloc[_i_stop]
#                 add_s(df.index[_i_stop], _candle.low if bullish(_candle) else _candle.high)
#                 i = i - 1  # уменьшить счетчик, тк при выходе из while добавлена лишняя 1
#         elif candle.low >= _candle.low:
#             while candle.low >= _candle.low:
#                 _candle = candle
#                 candle = df.iloc[i]
#                 i = i + 1
#             if i > _i:
#                 # print('up stop', i-1-1)
#                 _i_stop = i - 1 - 1
#                 _candle = df.iloc[_i_stop]
#                 add_s(df.index[_i_stop], _candle.low if bullish(_candle) else _candle.high)
#                 i = i - 1
#         else:
#             i = i + 1
#
#
#     # print(df.head(10))
#
#     _dt1 = dt1[0]
#     _s1 = stream1[0]
#     j = 1
#     while j < len(dt1):
#         fp.add_line((_dt1, _s1), (dt1[j], stream1[j]))
#         # fp.add_text((_dt1, _s1), '+')
#         _dt1 = dt1[j]
#         _s1 = stream1[j]
#         j = j + 1
#
#     fp.show()
