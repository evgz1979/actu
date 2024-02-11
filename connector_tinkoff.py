from tinkoff.invest.services import *

from candles import Interval
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
from tinkoff.invest.utils import now
import configparser


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


def convert_interval(interval):
    if interval == Interval.day1:
        return CandleInterval.CANDLE_INTERVAL_DAY
    elif interval == Interval.hour1:
        return CandleInterval.CANDLE_INTERVAL_HOUR
    elif interval == Interval.min5:
        return CandleInterval.CANDLE_INTERVAL_5_MIN
    elif interval == Interval.week1:
        return CandleInterval.CANDLE_INTERVAL_WEEK


# todo Для получения информации о дате начала истории добавлены параметры
# todo first_1min_candle_date и first_1day_candle_date в методах сервиса инструментов.

class TTinkoffAbstractConnector(TConnector):
    account_id = 0
    token = ''
    app_name = ''

    def __init__(self, config):
        super().__init__(config)
        self.token = config.get('CONNECTOR: TINKOFF', 'token')
        self.app_name = config.get('CONNECTOR: TINKOFF', 'app_name')

        with Client(self.token) as client:
            r = client.users.get_accounts()
            self.account_id = r.accounts[0].id

    def main(self):
        pass

    async def amain(self):
        pass


class TTinkoffHistoryConnector(TTinkoffAbstractConnector):
    def __init__(self, token):
        super().__init__(token)
        logger.info(">> Tinkoff history connector init")


class TTinkoffConnector(TTinkoffAbstractConnector):
    def __init__(self, token):
        super().__init__(token)
        logger.info(">> Tinkoff connector init")

    def get_futures(self, alias):

        with Client(self.token) as client:
            r1 = client.instruments.futures()

        futures = list(
            filter(lambda item: item.basic_asset == alias and now() < item.last_trade_date, r1.instruments))
        futures.sort(key=lambda item: item.last_trade_date)

        return futures

    def get_spot(self, name):

        with Client(self.token) as client:
            r1 = client.instruments.find_instrument(query=name)

        spot = list(r1.instruments)
        spot.sort(key=lambda item: item.name)

        return spot

    def show_settings(self):
        logger.info("account id = " + self.account_id)

    def get_candles_2(self, figi, interval):

        try:
            logger.info("start getting candles, symbol=" + figi + ", Interval=" + str(interval) + "...")

            if interval == Interval.day1:  # for Interval.day1 need absolutely all candles
                from_2 = now() - timedelta(days=100)
            else:
                from_2 = now() - timedelta(days=10)  # по каждому интервалу индивидуально

            with Client(self.token) as client:
                settings = MarketDataCacheSettings(base_cache_dir=Path("market_data_cache"))
                market_data_cache = MarketDataCache(settings=settings, services=client)

                r = []

                for candle in market_data_cache.get_all_candles(
                        figi=figi,
                        from_=from_2,
                        interval=convert_interval(interval)
                ):
                    r.append(TCandle(candle.time, cast_money(candle.open),
                                     cast_money(candle.high), cast_money(candle.low),
                                     cast_money(candle.close), cast_money(candle.volume), candle.is_complete))

            logger.info("...success")
            return r

        except Exception as ex:
            logger.error(ex)

    def get_candles(self, figi, interval, from2, to2):

        try:
            logger.info("start getting candles, symbol=" + figi + ", Interval=" + str(interval) + "...")

            # if interval == Interval.day1:  # for Interval.day1 need absolutely all candles
            #     from_2 = now() - timedelta(days=100)
            #     from_2 = self.config.get()
            # else:
            #     from_2 = now() - timedelta(days=10)  # по каждому интервалу индивидуально

            with Client(self.token) as client:
                settings = MarketDataCacheSettings(base_cache_dir=Path("market_data_cache"))
                market_data_cache = MarketDataCache(settings=settings, services=client)

                # for candle in market_data_cache.get_all_candles(
                #         figi=figi,
                #         from_=from_2,
                #         interval=convert_interval(interval)
                # ):
                #     print(candle.time)

                df = DataFrame(
                    [
                        {
                            'index': c.time.timestamp(),
                            'ts': c.time.timestamp(),
                            'open': cast_money(c.open),
                            'close': cast_money(c.close),
                            'high': cast_money(c.high),
                            'low': cast_money(c.low),
                            'volume': c.volume,
                            'dt': c.time
                        } for c in market_data_cache.get_all_candles(
                            figi=figi,
                            from_=from2,
                            interval=convert_interval(interval))
                    ]
                )

            logger.info("...success")
            return df.set_index('index')

        except Exception as ex:
            logger.error(ex)

    def _get_candles_old(self, symbol_name, interval):
        try:
            with Client(self.token) as client:
                r = client.market_data.get_candles(
                    figi=symbol_name,
                    from_=datetime.utcnow() - timedelta(days=7),
                    to=datetime.utcnow(),
                    interval=convert_interval(interval)
                )
        except Exception as ex:
            logger.error(ex)
        return create_df(r.data)

    async def task01(self, client):
        pass

    async def task02(self, client):
        pass

    def main(self):
        super().main()
        self.show_settings()  # -> gui

    async def amain(self):
        await super().amain()
        try:
            async with AsyncClient(self.token) as client:
                tasks = [asyncio.ensure_future(self.task01(client)),
                         asyncio.ensure_future(self.task02(client))]
                await asyncio.wait(tasks)
        except Exception as ex:
            logger.error(ex)
