from pandas import DataFrame
from base.info import *


class TCandlesDataFrame(DataFrame):
    dtfrom: datetime
    dtto: datetime
    # pass


class TOIData(DataFrame):
    pass


class CandlesList(list[TCandle]):
    dtload: (datetime, datetime)  # (from, to)
    dtcalc: (datetime, datetime)  # (from, to)
