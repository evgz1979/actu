import ccxt
from funcs import *
import pandas as pd

key = "VGBlKCHW0Thc0Qk63JvO2FE8Z7lDQpxxlriqgGR1g8ED5OdFgINLqrilvYvlCnze"
secret = "CjDOaNifYTCb7a2KmvGkAFtFOMKDy9dd3psflBzSlyek9rht0Xt1WRup37kxujtO"
symbol_name_bi = 'BTCUSDT'
symbol_name_ku = 'BTC/USDT' #{'spot': 'BTC/USDT', 'futures': 'BTC/USDT:USDT'}

kus = ccxt.kucoin({
    'enableRateLimit': True,
    'apiKey': '63923a46cc568b0001280c4f',
    'secret': 'c2bdd050-252f-4760-b663-a9fe1e6f8162',
    'password': 'vEcnab-wicbot-3gazga'})

kuf = ccxt.kucoinfutures({
    'enableRateLimit': True,
    'apiKey': '63923f2ba0afa6000112b79c',
    'secret': 'bf5dba3b-6af3-40ee-a833-9c35827fff3b',
    'password': 'api_nizwuv-rirWev-gepde9'})


def candles_to_df3(candles):  # temp function
    df = pd.DataFrame(candles, columns='ts open high low close volume'.split()).astype(
        {'ts': int, 'open': float, 'high': float, 'low': float, 'close': float, 'volume': float})
    df.insert(1, 'dt', '')
    df['dt'] = df.apply(lambda x: timestamp2iso(x['ts'], format='%Y-%m-%d %H:%M:%S'), axis=1)
    df.insert(1, 'interval', '1d')
    df.insert(1, 'symbol_id', 1)
    return df.set_index('ts')


def get_candles_old(s: str, interval):
    a = kus.fetch_ohlcv(s, interval, limit=500)
    return a


kus.load_markets()
kuf.load_markets({'future': True})






#time.sleep(ku_s.rateLimit / 1000)

#bis = ccxt.binance({'apiKey': 'VGBlKCHW0Thc0Qk63JvO2FE8Z7lDQpxxlriqgGR1g8ED5OdFgINLqrilvYvlCnze',
#                  'secret': 'CjDOaNifYTCb7a2KmvGkAFtFOMKDy9dd3psflBzSlyek9rht0Xt1WRup37kxujtO'})
#bis.load_markets()




# get_candles(quoted_symbols[0].name, 'D')
# df = candles_to_df3(get_candles_old(symbol_name_ku, '1d'))
# df.to_sql('candle', con=engine, if_exists='append')
# print(df)

# print('max=', df['high'].max(), '; min=', df['low'].min())
# fp.candlestick_ochl(df[['open', 'close', 'high', 'low']])
# fp.show()

