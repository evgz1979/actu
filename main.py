from datafeed import *
from datetime import datetime
import pandas as pd
import mplfinance as mpf
import finplot as fp


print('>> actualiZator started')

# get_candles(quoted_symbols[0].name, 'D')
df = candles_to_df3(get_candles_old(symbol_name_ku, '1d'))
# df.to_sql('candle', con=engine, if_exists='append')
# print(df)

# print('max=', df['high'].max(), '; min=', df['low'].min())
fp.candlestick_ochl(df[['open', 'close', 'high', 'low']])
fp.show()

df = pd.read_csv('db/rts01.csv',
                 dtype={'date': str, 'time': str,
                        'open': float, 'high': float, 'low': float, 'close': float,
                        'volume': float})
df['dt'] = pd.to_datetime(df['date'] + df['time'])
# df.insert(0, 'ts', 0)
df.drop('date', axis=1, inplace=True)
df.drop('time', axis=1, inplace=True)
# df['ts'] = df.apply(lambda x: iso2timestamp(x['dt'], format='%Y%m%d %H%M%S'), axis=1)
# df.drop('dt', axis=1, inplace=True)
# df.set_index('dt')
df.index.name = 'dt'
df.index = pd.DatetimeIndex(df['dt'])

print(df)

mpf.plot(df, type='candle', warn_too_much_data=1000)

