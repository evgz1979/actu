# actualiZator, (c) jz

from datafeed import *
from drawer import *

# ku = TKUCoinConnector()
# tink = TTinkoffConnector()

data = TDataFeeder(quoted_symbol_00)
data.load_from_db()
# data.print_0()

qs1 = data.quoted[0]

print(qs1.name)


candles1 = data.quoted[0].get_candles('1d')

# for candle in candles1:
#     print(candle.open)


# df = load_from_file('db/rts01.csv')
# draw1(df)






