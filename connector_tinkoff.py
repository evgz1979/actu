from connector import *
import asyncio
from datetime import timedelta
from pathlib import Path
from tinkoff.invest.caching.market_data_cache.cache import MarketDataCache
from tinkoff.invest.caching.market_data_cache.cache_settings import MarketDataCacheSettings
from pandas import DataFrame
from funcs import *
import pandas as pd
from tinkoff.invest import CandleInterval, Client, HistoricCandle, AsyncClient
from tinkoff.invest.utils import now
from settings import *
from orm import *


def create_df(candles: [HistoricCandle]):  # -> tink_connector.py
    df = DataFrame([{
        'time': c.time,
        'volume': c.volume,
        'open': cast_money(c.open),
        'close': cast_money(c.close),
        'high': cast_money(c.high),
        'low': cast_money(c.low),
    } for c in candles])

    return df


class TTinkoffConnector(TMOEXConnector):
    account_id = 0
    TOKEN = ''

    def __init__(self, token):
        logger.info(">> Tinkoff connector init")

        self.TOKEN = token

        with Client(self.TOKEN) as client:
            r = client.users.get_accounts()
            self.account_id = r.accounts[0].id

    def show_settings(self):
        logger.info("account id = " + self.account_id)

    def get_test01(self):
        with Client(token_tinkoff_all_readonly) as client:
            settings = MarketDataCacheSettings(base_cache_dir=Path("market_data_cache"))
            market_data_cache = MarketDataCache(settings=settings, services=client)
            for candle in market_data_cache.get_all_candles(
                    figi="BBG004730N88",
                    from_=now() - timedelta(days=3),
                    interval=CandleInterval.CANDLE_INTERVAL_1_MIN,
            ):
                print(candle.time)

    def convert_interval(self, interval):
        if interval == TInterval.day1: return CandleInterval.CANDLE_INTERVAL_DAY
        elif interval == TInterval.hour1: return CandleInterval.CANDLE_INTERVAL_HOUR
        elif interval == TInterval.min5: return CandleInterval.CANDLE_INTERVAL_5_MIN

    def get_candles(self, symbol_name, interval):
        try:
            with Client(self.TOKEN) as client:
                r = client.market_data.get_candles(
                    figi=symbol_name,
                    from_=datetime.utcnow() - timedelta(days=7),
                    to=datetime.utcnow(),
                    interval=self.convert_interval(interval)
                )
        except Exception as ex:
            logger.error(ex)
        return create_df(r.candles)

    async def task01(self, client):
        pass

    async def task02(self, client):
        pass

    def main(self):
        self.show_settings()  # -> gui

    async def amain(self):
        try:
            async with AsyncClient(self.TOKEN) as client:
                tasks = [asyncio.ensure_future(self.task01(client)),
                         asyncio.ensure_future(self.task02(client))]
                await asyncio.wait(tasks)
        except Exception as ex:
            logger.error(ex)

