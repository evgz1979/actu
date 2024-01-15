from connector import *
from orm import *
from datetime import datetime
from typing import Optional, List
import configparser
from candles import *


class TCandles(DataFrame):
    # переопредлить init --- сразу выставлять названия слобцов и индекс
    pass


class TCandlesCollection:
    week1: TCandles
    day1: TCandles
    hour1: TCandles
    min5: TCandles


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

    candles: TCandlesCollection  # so far so

    def __init__(self, name, ticker, figi, connector, **kwargs):
        self.name = name
        self.ticker = ticker
        self.figi = figi
        self.connector = connector
        self.is_future = kwargs.get('future', False)
        self.is_spot = kwargs.get('spot', False)
        self.quoted = kwargs.get('quoted', False)

        self.candles = TCandles()


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

    connector: TConnector
    config: configparser.ConfigParser

    def __init__(self, alias, connector, config):
        self.connector = connector
        self.config = config

        self.alias = alias
        self.name = config.get('META: ' + alias, 'name')

    def main(self):
        for symbol in self.symbols:
            logger.info(f"name={symbol.name}, ticker={symbol.ticker}, figi={symbol.figi}, quoted={symbol.quoted}")

        from22 = datetime.strptime(
            self.config.get('META: ' + self.alias, 'from_day_current_situation'), '%Y-%m-%d').astimezone(now().tzinfo)

        self.spot_T0.candles.day1 = \
            self.spot_T0.connector.get_candles(self.spot_T0.figi, Interval.day1, from22, now())

        # self.spot_T0.candles.week1 = \
        #     self.spot_T0.connector.get_candles(self.spot_T0.figi, Interval.week1, from22, now())
        #
        # self.future_current.candles.day1 = \
        #     self.spot_T0.connector.get_candles(self.future_current.figi, Interval.day1, from22, now())
        #
        # self.future_current.candles.week1 = \
        #     self.spot_T0.connector.get_candles(self.future_current.figi, Interval.week1, from22, now())
