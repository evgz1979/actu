from datafeed import *
from drawer import *
from datetime import datetime
import pandas as pd
import mplfinance as mpf
import finplot as fp

print('>> actualiZator started')

df = load_file('db/rts01.csv')

draw1(df)


