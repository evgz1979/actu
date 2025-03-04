import asyncio
from datetime import time
import logging
import os
from datetime import timedelta
from pathlib import Path
import ccxt
from ccxt import kucoin, kucoinfutures
from tinkoff.invest.caching.market_data_cache.cache import MarketDataCache
from tinkoff.invest.caching.market_data_cache.cache_settings import MarketDataCacheSettings
from pandas import DataFrame
from funcs import *
import pandas as pd
from tinkoff.invest import CandleInterval, Client, HistoricCandle, AsyncClient
from tinkoff.invest.utils import now
from settings import *
from orm import *
import configparser

# key = "VGBlKCHW0Thc0Qk63JvO2FE8Z7lDQpxxlriqgGR1g8ED5OdFgINLqrilvYvlCnze"
# secret = "CjDOaNifYTCb7a2KmvGkAFtFOMKDy9dd3psflBzSlyek9rht0Xt1WRup37kxujtO"
# symbol_name_bi = 'BTCUSDT'
# symbol_name_ku = 'BTC/USDT'  # {'spot': 'BTC/USDT', 'futures': 'BTC/USDT:USDT'}


class Trader:
    pass


class TConnector:
    id = ''

    trader: Trader = None

    def __init__(self, _id):
        self.id = _id
        pass

    def get_candles(self, symbol_name, interval, dtload):
        pass

    def get_by_asset(self, alias):
        pass

    def main(self):
        pass

    def amain(self):
        pass

    def get_oi(self, symbol, from_date: datetime = None, to_date: datetime = None):
        pass

    def get_info(self, ticker):
        return ticker


class YFinanceConnector(TConnector):
    pass


class TPoligonIOConnector(TConnector):
    pass


class TCryptoConnector(TConnector):
    pass


class TConnectors(list[TConnector]):

    def append(self, __object: TConnector) -> TConnector:
        super().append(__object)
        return __object

    def find_connector(self, _id):
        for c in self:
            if c.id == _id: return c

    def main(self):
        for connector in self:
            connector.main()

# class TKUCoinConnector(TCryptoConnector):
#     spot = kucoin
#     futures = kucoinfutures
#
#     def __init__(self):
#         self.spot = ccxt.kucoin({'enableRateLimit': True,
#                                  'apiKey': ku_spot_apikey, 'secret': ku_spot_secret, 'password': ku_spot_password})
#
#         self.futures = ccxt.kucoinfutures({'enableRateLimit': True,
#                                            'apiKey': ku_futures_apikey,
#                                            'secret': ku_futures_secret,
#                                            'password': ku_futures_password})
#
#         self.spot.load_markets()
#         self.futures.load_markets({'future': True})
#
#         # print(">> KU-Coin connector init")
#
#     def get_candles_df(self, s: str, interval):
#         candles = self.spot.fetch_ohlcv(s, interval, limit=500)
#
#         df = pd.DataFrame(candles, columns='ts open high low close volume'.split()).astype(
#             {'ts': int, 'open': float, 'high': float, 'low': float, 'close': float, 'volume': float})
#         df.insert(1, 'dt', '')
#         df['dt'] = df.apply(lambda x: timestamp2iso(x['ts'], format='%Y-%m-%d %H:%M:%S'), axis=1)
#         df.insert(1, 'interval', '1d')
#         df.insert(1, 'symbol_id', 1)
#         return df.set_index('ts')

# get_candles(quoted_symbols[0].name, 'D')
# df = candles_to_df3(get_candles_old(symbol_name_ku, '1d'))
# df.to_sql('candle', con=engine, if_exists='append')
# print(df)

# print('max=', df['high'].max(), '; min=', df['low'].min())
# fp.candlestick_ochl(df[['open', 'close', 'high', 'low']])
# fp.show()
