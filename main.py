from orm import *
from datafeed import *
import finplot as fp
from datetime import datetime

if __name__ == '__main__':
    print('>> actualiZator started')
    # get_candles(symbol_name_ku, 'D', datetime.now(), datetime.now())
    # df = candles_to_df3(get_candles_old(symbol_name_ku, '1w'))
    # df.to_sql('candle', con=engine, if_exists='append')
    # print(df)
    # print('max=', df['high'].max(), '; min=', df['low'].min())
    # fp.candlestick_ochl(df[['open', 'close', 'high', 'low']])
    # fp.show()

    print(len(quoted_symbols))
    print('quoted symbols:')
    for s in quoted_symbols:
        print('...', s)
