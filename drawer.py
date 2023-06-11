import finplot as fp
import numpy as np
import pandas as pd


def draw1(df):
    fp.background = '#cfc'
    fp.candle_bull_color = '#336'
    fp.candle_bear_color = '#6c9'
    fp.candle_bull_body_color = '#336'
    fp.candlestick_ochl(df[['open', 'close', 'high', 'low']])

    # dates = pd.date_range('01:00', '01:00:01.200', freq='1ms')
    # prices = pd.Series(np.random.random(len(dates))).rolling(30).mean() + 4
    # fp.plot(dates, prices, width=1)

    stream1 = []
    dt1 = []

    prev_row = None                              # --- расчеты потом убрать из drawer
    for index, row in df.iterrows():
        if prev_row is None:
            pass
        else:
            if prev_row['close'] == row['open']:
                dt1.append(index)
                stream1.append(row['open'])
        prev_row = row

    print(dt1)
    print(stream1)

    fp.plot(dt1, stream1, width=3)
    fp.show()

