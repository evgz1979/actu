from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

sqlite_url = f"sqlite:///db/01.db"
engine = create_engine(sqlite_url, echo=False)


class Symbol(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    exchange_name: str
    exchange_section: str
    dt_analyzer_start_from: datetime
    dt_historical_start: datetime
    quoted: bool

    candles: List["Candle"] = Relationship(back_populates="symbol")

    def get_candles(self, interval: str):  # , dt_from: datetime, dt_to: datetime):
        # print('>> get_candles:', self.name, interval)  # , 'dt:', dt_from, ' -> ', dt_to, ')')

        with Session(engine) as session:
            statement = select(Candle)
            results = session.exec(statement)
            return results

            # for candle in results:
            #    print(candle.open)

            # if results.first() is None: -- not work
            #    print('no one candle')


class Candle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    interval: str
    ts: int
    dt: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    symbol_id: Optional[int] = Field(default=None, foreign_key="symbol.id")
    symbol: Optional[Symbol] = Relationship(back_populates="candles")


class TCandle:
    _orm: Candle


class TInterval:
    name: str
    candles: List[TCandle]

    def __init__(self, name):
        self.name = name


class TSymbol:
    _orm: Symbol
    d1: TInterval
    h1: TInterval
    h2: TInterval

    def __init__(self):
        self.d1 = TInterval('d1')
        self.h1 = TInterval('h1')
        self.h2 = TInterval('h2')


# print(">> orm init")
SQLModel.metadata.create_all(engine)
