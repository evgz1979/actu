from connector import *
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

    def refresh(self):
        pass


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


quoted_symbols = []
quoted_symbol_0 = Symbol(name='BTC/USDT', exchange_name='kucoin', exchange_section='spot',
                         dt_analyzer_start_from=datetime.now(), dt_historical_start=datetime.now(), quoted=True)


def get_quoted_symbols():
    with Session(engine) as session:
        statement = select(Symbol).where(Symbol.quoted)

        results = session.exec(statement)
        for symbol in results:
            quoted_symbols.append(symbol)

        if len(quoted_symbols) == 0:
            session.add(quoted_symbol_0)
            session.commit()

            results = session.exec(statement)
            for symbol in results:
                quoted_symbols.append(symbol)


def get_candles(symbol_name: str, interval: str):  # , dt_from: datetime, dt_to: datetime):
    print('>> get_candles(', symbol_name, ', ', interval, ')')  # , 'dt:', dt_from, ' -> ', dt_to, ')')

    with Session(engine) as session:
        statement = select(Candle)
        results = session.exec(statement)
        if results.first() is None:
            print('no one candle')  # и нужно закачивать -- или провкерять что нужного количества нет то тоже обновлять через коннектор


print('>> datafeed init')
SQLModel.metadata.create_all(engine)

get_quoted_symbols()
print('quoted symbols:')
for qs in quoted_symbols:
    print('*', qs.name, '... please wait while quoted symbol refreshing candles data ...')
    qs.refresh

# ----
# --- это реализация с другой проги df = pd.DataFrame(r.json()['data']).astype({'timestamp':int, 'open':float, 'close':float, 'high':float, 'low':float}).set_index('timestamp')
