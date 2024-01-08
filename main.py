# ACTUaliZator, (c) JZ

from drawer import *
from trader import *
from datafeed import *
from ta.trend import ema_indicator
from tinkoff.invest import Client, RequestError, CandleInterval
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from connector_tinkoff import *
from connector import *
import configparser


if __name__ == "__main__":

    data = TDataFeeder()
    c_tink = TTinkoffConnector(data.config)
    data.connectors.append(c_tink)
    ms1 = TMetaSymbol('USD/RUB', c_tink, data.config)
    data.meta_symbols.append(ms1)

    trader = JZTrader(data)
    data.main()  # -> robot.main(data, trader, drawer) ?

    draw3(ms1.current_spot.candles.day1)

