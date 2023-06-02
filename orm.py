from datetime import datetime
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select


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


class Candle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    interval: int
    ts: int
    dt: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


print(">> orm init")
SQLModel.metadata.create_all(engine)



