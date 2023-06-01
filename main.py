from orm import *
from data import *
import finplot as fp

if __name__ == '__main__':
    df = candles_to_df3(get_candles(symbol_name, '1w'))  # -- так работает с базой
    print(df)
    print('max=', df['high'].max(), '; min=', df['low'].min())
    fp.candlestick_ochl(df[['open', 'close', 'high', 'low']])
    fp.show()  # унифицировать df для базы и графика
    df.to_sql('candles', con=engine, if_exists='append')  # потом удалить неуник значения

