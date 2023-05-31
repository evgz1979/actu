-- # infinity candle - одна свеча на весь график?

from _old_download import *
import finplot as fplt
from binance.spot import Spot
from settings import *

spot = Spot(key, secret)
df = get_data(spot, symbol=symbol, start_time='2021-01-10', end_time='2022-05-25', interval='1d')
fplt.candlestick_ochl(df[['open', 'close', 'high', 'low']])

# monthly separator lines
months = pd.to_datetime(df.index, unit='s').strftime('%m')
last_month = ''
for x, (month, price) in enumerate(zip(months, df.close)):
    if month != last_month:
        fplt.add_line((x-0.5, price*0.5), (x-0.5, price*2), color='#bbb', style='--')
    last_month = month

fplt.show()
------
df = download_price_history(interval_mins=30)  # reduce to [15, 5, 1] minutes to increase accuracy
time_volume_profile = calc_volume_profile(df, period='W', bins=100)  # try fewer/more horizontal bars (graphical resolution only)
vwap = calc_vwap(df, period='W')  # try period='D'
fplt.create_plot('Binance BTC futures weekly volume profile')
fplt.create_plot('Binance BTC futures weekly volume profile')
fplt.plot(df.time, df.close, legend='Price')
fplt.plot(df.time, vwap, style='--', legend='VWAP')
fplt.horiz_time_volume(time_volume_profile, draw_va=0.7, draw_poc=1.0)
fplt.show()

----

from _old_download import *
import finplot as fplt
from binance.spot import Spot
from settings import *

spot = Spot(key, secret)
df = get_data(spot, symbol=symbol, start_time='2022-04-10', end_time='2022-05-21', interval='1d')
fplt.candlestick_ochl(df[['open', 'close', 'high', 'low']])
fplt.show()
---



# pip install finplot==1.8.0
# перенести Models + DB
# удалить все остальные проекты чтобы не путаться

# pip install finplot==1.8.0
# binance-public-data ------- on github
# pip install binance-connector
# pip install binance-futures-connector
# pip install peewee

from _old_download import *
from _old_models import *
import logging
from binance.futures import Futures
from binance.spot import Spot
from binance.lib.utils import config_logging
from binance.error import ClientError
import finplot as fplt
import yfinance
import pandas as pd
import numpy as np

key = "VGBlKCHW0Thc0Qk63JvO2FE8Z7lDQpxxlriqgGR1g8ED5OdFgINLqrilvYvlCnze"
secret = "CjDOaNifYTCb7a2KmvGkAFtFOMKDy9dd3psflBzSlyek9rht0Xt1WRup37kxujtO"

# config_logging(logging, logging.DEBUG)
# db_create()

# spot = Spot(key, secret)
# futures = Futures(key, secret, base_url="https://fapi.binance.com")

# try:
#     response = futures.balance(recvWindow=6000)
# print('balance: ', response)
# except ClientError as error:
#     logging.error(
#         "Found error. status: {}, error code: {}, error message: {}".format(
#             error.status_code, error.error_code, error.error_message
#         )
#     )
# print(spot.account())
# print(futures.account())
# print(spot.time())

# print(spot.klines("BTCUSDT", "1h", limit=10))

# df = download1(symbol='BTCUSDT', start_time='2022-05-09', end_time='2022-05-19', interval=30)
df = download0(symbol='BTCUSDT', start_time='2020-09-01', end_time='2022-05-21', interval=240)
# df = download1(symbol='BTCUSDT', start_time='2022-05-16', end_time='2022-05-19', interval=5)
df['dt_open'] = pd.to_datetime(df['dt_open'])
df = df.set_index('dt_open')
print(df)
fplt.candlestick_ochl(df[['open', 'close', 'high', 'low']])
fplt.show()

# df = yfinance.download('AAPL')
# print(df)
# fplt.candlestick_ochl(df[['Open', 'Close', 'High', 'Low']])
# fplt.show()


---
a1()
пытался чтото начать считать по свечам
def a1():
    i = 0
    while i < len(df) - 1:
        i = i + 1
        row_prev = df.iloc[i - 1]
        row = df.iloc[i]
        if (row['low'] < row_prev['low']) and (row['high'] < row_prev['high']):
            fplt.add_line((i - 1, row_prev['high']), (i + 9, row_prev['high']), color='#9900ff')


---
'timeframes': {
    '1m': '1min',
    '3m': '3min',
    '5m': '5min',
    '15m': '15min',
    '30m': '30min',
    '1h': '1hour',
    '2h': '2hour',
    '4h': '4hour',
    '6h': '6hour',
    '8h': '8hour',
    '12h': '12hour',
    '1d': '1day',
    '1w': '1week',