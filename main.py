# ACTUaliZator, (c) JZ

from datafeed import *
from ta.trend import ema_indicator
from tinkoff.invest import Client, RequestError, CandleInterval
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from connector_tinkoff import *


def draw01():
    df['ema'] = ema_indicator(close=df['close'], window=9)

    print(df[['time', 'close', 'ema']].tail(5))
    ax = df.plot(x='time', y='close')
    df.plot(ax=ax, x='time', y='ema')
    plt.show()


if __name__ == "__main__":
    data = TDataFeeder()
    data.connectors['tink1'] = conn1 = TTinkoffConnector(token_tinkoff_all_readonly)
    data.symbols.append(TSymbol('USD000UTSTOM', 'tink1'))
    data.main()

    df = conn1.get_candles()  # -> data.main()
    draw01()  # -> drawer

    data.amain()

