# --- работает: с бинанса берет данные и выводит на график ---

from _old_download import *
import finplot as fplt
from binance.spot import Spot
from connector import *

spot = Spot(key, secret)
symbol = spot.exchange_info(symbol_name)
df = get_data(spot, symbol=symbol_name, start_time='2014-12-01', end_time='2022-07-26', interval='1w')
fplt.candlestick_ochl(df[['open', 'close', 'high', 'low']])
fplt.show()
print('max=', df['high'].max())
print('min=', df['low'].min())

-------worked!!!
from _old_download import *
import finplot as fplt
from binance.spot import Spot
from connector import *

spot = Spot(key, secret)
symbol = spot.exchange_info(symbol_name)
df = get_data(spot, symbol=symbol_name, start_time='2014-12-01', end_time='2022-07-26', interval='1w')
fplt.candlestick_ochl(df[['open', 'close', 'high', 'low']])
fplt.show()
print('max=', df['high'].max())
print('min=', df['low'].min())

----------
c1 = Customer(
    first_name='Dmitriy',
    last_name='Yatsenko',
    username='Moseend',
    email='moseend@mail.com'
)

c2 = Customer(
    first_name='Valeriy',
    last_name='Golyshkin',
    username='Fortioneaks',
    email='fortioneaks@gmail.com'
)

print(c1.first_name, c2.last_name)


session.add(c1)
session.add(c2)

print(session.new)

session.commit()