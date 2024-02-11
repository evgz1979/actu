from connector import *
from connector_moex import *
from orm import *
from datetime import datetime
from typing import Optional, List
import configparser
from candles import *
import pandas as pd


class TSymbol:
    name = ''
    ticker = ''
    figi = ''

    quoted = False
    is_future = False
    is_spot = False

    connector: TConnector
    _orm_symbol: Symbol
    _orm_candle: Candle

    data: TCandlesCollectionData  # so far so
    candles: TCandlesCollection  # so far so

    def __init__(self, name, ticker, figi, connector, **kwargs):
        self.name = name
        self.ticker = ticker
        self.figi = figi
        self.connector = connector
        self.is_future = kwargs.get('future', False)
        self.is_spot = kwargs.get('spot', False)
        self.quoted = kwargs.get('quoted', False)

        self.data = TCandlesCollectionData()
        self.open_interest_data = TOICollectionData()
        self.candles = TCandlesCollection()

    def refresh(self):

        # for day1 interval
        self.candles.day1.clear()
        i = 0
        while i < self.data.day1.shape[0]:
            d = self.data.day1.iloc[i]
            # print(d)

            c = TCandle(
                d['ts'], d['dt'], d['open'], d['high'], d['low'], d['close'], d['volume'], True
            )

            self.candles.day1.append(c)
            # print(c.dt, c.ts)

            i = i+1

        self.candles.max_all_high = self.data.day1['high'].max()
        self.candles.min_all_low = self.data.day1['low'].min()

        # print(self.candles.max_all_high)
        # print(self.candles.min_all_low)


class TMetaSymbol:
    name = ''
    alias = ''
    # figi = ''
    # future = ''
    # description = ''

    symbols = []
    future_current: TSymbol = None
    future_infinity: TSymbol = None
    spot_T0: TSymbol = None
    spot_T1: TSymbol = None
    spot_T2: TSymbol = None

    connector: TConnector  # todo --> унифицировать
    moex: TMOEXConnector  # todo --> унифицировать

    config: configparser.ConfigParser

    def __init__(self, alias, connector, moex, config):
        self.connector = connector
        self.moex = moex
        self.config = config

        self.alias = alias
        self.name = config.get('META: ' + alias, 'name')

    def main(self):
        for symbol in self.symbols:
            logger.info(f"name={symbol.name}, ticker={symbol.ticker}, figi={symbol.figi}, quoted={symbol.quoted}")

        from22 = datetime.strptime(
            self.config.get('META: ' + self.alias, 'from_day_current_situation'), '%Y-%m-%d').astimezone(now().tzinfo)

        self.spot_T0.data.day1 = \
            self.spot_T0.connector.get_candles(self.spot_T0.figi, Interval.day1, from22, now())

        # todo - без дат!!! - запрашивать у DataFeeder (у него всегда все готово должно быть)
        self.future_current.open_interest_data.day1\
            = self.moex.get_futures_oi(symbol='si', from_date=from22, to_date=now())

        # print(self.future_current.open_interest_data.day1)

