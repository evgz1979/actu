from datetime import datetime
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select


sqlite_url = f"sqlite:///db/01.db"
engine = create_engine(sqlite_url, echo=True)


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


if __name__ == '__main__':
    SQLModel.metadata.create_all(engine)
