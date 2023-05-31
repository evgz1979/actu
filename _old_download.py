import pandas as pd
import requests
import pytz
import dateutil.parser
from _old_models import *
from binance.spot import Spot
from collections import defaultdict

utc2timestamp = lambda s: int(dateutil.parser.parse(s).replace(tzinfo=pytz.utc).timestamp() * 1000)


def download_price_history(symbol='BTCUSDT', start_time='2020-06-22', end_time='2020-08-19', interval_mins=1):
    interval_ms = 1000 * 60 * interval_mins
    interval_str = '%sm' % interval_mins if interval_mins < 60 else '%sh' % (interval_mins // 60)
    start_time = utc2timestamp(start_time)
    end_time = utc2timestamp(end_time)
    data = []
    for start_t in range(start_time, end_time, 1000 * interval_ms):
        end_t = start_t + 1000 * interval_ms
        if end_t >= end_time:
            end_t = end_time - interval_ms
        url = 'https://www.binance.com/fapi/v1/klines?interval=%s&limit=%s&symbol=%s&startTime=%s&endTime=%s' % (
            interval_str, 1000, symbol, start_t, end_t)
        print(url)
        d = requests.get(url).json()
        data += d
    df = pd.DataFrame(data, columns='time open high low close volume a b c d e f'.split())
    return df.astype(
        {'time': 'datetime64[ms]', 'open': float, 'high': float, 'low': float, 'close': float, 'volume': float})


def calc_volume_profile(df, period, bins):
    '''Calculate a poor man's volume distribution/profile by "pinpointing" each kline volume to a certain
       price and placing them, into N buckets. (IRL volume would be something like "trade-bins" per candle.)
       The output format is a matrix, where each [period] time is a row index, and even columns contain
       start (low) price and odd columns contain volume (for that price and time interval). See
       finplot.horiz_time_volume() for more info.'''
    data = []
    df['hlc3'] = (df.high + df.low + df.close) / 3  # assume this is volume center per each 1m candle
    _, all_bins = pd.cut(df.hlc3, bins, right=False, retbins=True)
    for _, g in df.groupby(pd.Grouper(key='time', freq=period)):
        t = g.time.iloc[0]
        volbins = pd.cut(g.hlc3, all_bins, right=False)
        price2vol = defaultdict(float)
        for iv, vol in zip(volbins, g.volume):
            price2vol[iv.left] += vol
        data.append([t, sorted(price2vol.items())])
    return data


def calc_vwap(df, period):
    vwap = pd.Series([], dtype='float64')
    df['hlc3v'] = df['hlc3'] * df.volume
    for _, g in df.groupby(pd.Grouper(key='time', freq=period)):
        i0, i1 = g.index[0], g.index[-1]
        vwap = vwap.append(g.hlc3v.loc[i0:i1].cumsum() / df.volume.loc[i0:i1].cumsum())
    return vwap


def download_v3(spot: Spot, symbol, start_time, end_time, interval):
    data = spot.klines(symbol, interval, startTime=utc2timestamp(start_time), endTime=utc2timestamp(end_time),
                       limit='1000')
    df = pd.DataFrame(data,
                      columns='dt_open open high low close volume dt_close quote_asset_volume trades_count taker_buy_volume taker_buy_quote_asset_volume interest_or_ignore'.split()).astype(
        {'dt_open': 'datetime64[ms]', 'open': float, 'high': float, 'low': float, 'close': float, 'volume': float,
         'dt_close': 'datetime64[ms]', 'quote_asset_volume': float, 'trades_count': float,
         'taker_buy_volume': float, 'taker_buy_quote_asset_volume': float, 'interest_or_ignore': float})
    df['dt_open'] = pd.to_datetime(df['dt_open'])
    df['dt_close'] = pd.to_datetime(df['dt_close'])
    df = df.set_index('dt_open')
    return df


def download_v3_1(spot: Spot, symbol, start_time, end_time, interval):
    data = spot.klines(symbol, interval, startTime=utc2timestamp(start_time), endTime=utc2timestamp(end_time), limit='1000')
    df = pd.DataFrame(data,
                      columns='dt_open open high low close volume dt_close quote_asset_volume trades_count taker_buy_volume taker_buy_quote_asset_volume interest_or_ignore'.split()).astype(
        {'dt_open': int, 'open': float, 'high': float, 'low': float, 'close': float, 'volume': float,
         'dt_close': int, 'quote_asset_volume': float, 'trades_count': float,
         'taker_buy_volume': float, 'taker_buy_quote_asset_volume': float, 'interest_or_ignore': float})
    # df['dt_open'] = pd.to_datetime(df['dt_open'])
    # df['dt_close'] = pd.to_datetime(df['dt_close'])
    # df = df.set_index('dt_open')
    return df


def get_data(spot: Spot, symbol, start_time, end_time,
             interval):  # пока все онлайн, позже организовать кэш в базу и паралельное скачивание нужных данных
    return download_v3(spot, symbol, start_time, end_time, interval)


def download0(symbol, start_time, end_time, interval):
    interval_ms = 1000 * 60 * interval
    interval_str = '%sm' % interval if interval < 60 else '%sh' % (interval // 60)
    start_time = utc2timestamp(start_time)
    end_time = utc2timestamp(end_time)
    data = []
    for start_t in range(start_time, end_time, 1000 * interval_ms):
        end_t = start_t + 1000 * interval_ms
        if end_t >= end_time:
            end_t = end_time - interval_ms
        url = 'https://www.binance.com/api/v1/klines?interval=%s&limit=%s&symbol=%s&startTime=%s&endTime=%s' % (
            interval_str, 1000, symbol, start_t, end_t)
        print(url)
        d = requests.get(url).json()
        data += d

    df = pd.DataFrame(data,
                      columns='dt_open open high low close volume dt_close quote_asset_volume trades_count taker_buy_volume taker_buy_quote_asset_volume interest_or_ignore'.split()).astype(
        {'dt_open': 'datetime64[ms]', 'open': float, 'high': float, 'low': float, 'close': float, 'volume': float,
         'dt_close': float, 'quote_asset_volume': float, 'trades_count': float,
         'taker_buy_volume': float, 'taker_buy_quote_asset_volume': float, 'interest_or_ignore': float})
    df['dt_open'] = pd.to_datetime(df['dt_open'])
    df = df.set_index('dt_open')
    return df


def download1(symbol, start_time, end_time, interval):
    interval_ms = 1000 * 60 * interval
    interval_str = '%sm' % interval if interval < 60 else '%sh' % (interval // 60)
    start_time = utc2timestamp(start_time)
    end_time = utc2timestamp(end_time)
    data = []
    for start_t in range(start_time, end_time, 1000 * interval_ms):
        end_t = start_t + 1000 * interval_ms
        if end_t >= end_time:
            end_t = end_time - interval_ms
        url = 'https://www.binance.com/api/v1/klines?interval=%s&limit=%s&symbol=%s&startTime=%s&endTime=%s' % (
            interval_str, 1000, symbol, start_t, end_t)
        print(url)
        d = requests.get(url).json()
        data += d

    df = pd.DataFrame(data,
                      columns='dt_open open high low close volume dt_close quote_asset_volume trades_count taker_buy_volume taker_buy_quote_asset_volume interest_or_ignore'.split()).astype(
        {'dt_open': 'datetime64[ms]', 'open': float, 'high': float, 'low': float, 'close': float, 'volume': float,
         'dt_close': float, 'quote_asset_volume': float, 'trades_count': float,
         'taker_buy_volume': float, 'taker_buy_quote_asset_volume': float, 'interest_or_ignore': float})

    for i, row in df.iterrows():
        #    print(f"Index: {i}")
        #    print(f"{row}\n")
        dict2 = row.to_dict()
        dict2['symbol_id'] = 0
        dict2['interval'] = interval
        dict2['volume_profile'] = '*'

        # candle = Candle.create()
        # print(dict2)
        # candle = Candle.create(dict2)
        # v1 = Candle.insert(dict2).execute

        candle = Candle.create(
            symbol_id=dict2['symbol_id'],
            interval=dict2['interval'],
            dt_open=0,
            open=dict2['open'],
            high=dict2['high'],
            low=dict2['low'],
            close=dict2['close'],
            volume=dict2['volume'],
            dt_close=0,
            quote_asset_volume=dict2['quote_asset_volume'],
            trades_count=dict2['trades_count'],
            taker_buy_volume=dict2['taker_buy_volume'],
            taker_buy_quote_asset_volume=dict2['taker_buy_quote_asset_volume'],
            interest_or_ignore=dict2['interest_or_ignore'],
            volume_profile=dict2['volume_profile']
        )
        candle.save()
    print(i, 'non-unique items store in db')
    df['dt_open'] = pd.to_datetime(df['dt_open'])
    df = df.set_index('dt_open')
    return df


def get_symbols(symbol):
    interval_ms = 1000 * 60 * interval
    interval_str = '%sm' % interval if interval < 60 else '%sh' % (interval // 60)
    start_time = utc2timestamp(start_time)
    end_time = utc2timestamp(end_time)
    data = []
    for start_t in range(start_time, end_time, 1000 * interval_ms):
        end_t = start_t + 1000 * interval_ms
        if end_t >= end_time:
            end_t = end_time - interval_ms
        url = 'https://www.binance.com/fapi/v1/klines?interval=%s&limit=%s&symbol=%s&startTime=%s&endTime=%s' % (
            interval_str, 1000, symbol, start_t, end_t)
        print(url)
        d = requests.get(url).json()
        data += d

#    symbol_id = ForeignKeyField(Symbol)
#    interval = IntegerField()
#    dt_open = DateTimeField()
#    open = FloatField()
#    high = FloatField()
#    low = FloatField()
#    close = FloatField()
#    volume = FloatField()
#    dt_close = DateTimeField()
#    quote_asset_volume = FloatField()
#    trades_count = IntegerField()
#    taker_buy_volume = FloatField()
#    taker_buy_quote_asset_volume = FloatField()
#    interest_or_ignore = FloatField()
#    volume_profile = CharField()

#   1607444700000,          // Open time
#    "18879.99",             // Open
#    "18900.00",             // High
#    "18878.98",             // Low
#    "18896.13",             // Close (or latest price)
#    "492.363",              // Volume
# a    1607444759999,          // Close time
# b    "9302145.66080",        // Quote asset volume
# c    1874,                   // Number of trades
# d    "385.983",              // Taker buy volume
# e    "7292402.33267",        // Taker buy quote asset volume
# f    "0"                     // Ignore.
