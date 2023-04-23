from sqlalchemy import create_engine, MetaData, Table, Integer, Float, String, \
    Column, DateTime, ForeignKey, Numeric, SmallInteger

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime


Base = declarative_base()

# все инициализации базы, проверка на таблицы, если что создаю, если базы нет - создаю и служебные таблицы по умолчанию из констант создаю
# проверка на полноту данных (например по свечам для котируемых инструментов) и на дубли и корректность (на валидность короче) и др
class DbEngine:
    pass


class Interval(Base):
    __tablename__ = 'intervals'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), nullable=False)
    comment = Column(String(100), nullable=False)


class Candle(Base):
    __tablename__ = 'candles'
    id = Column(Integer(), primary_key=True)
    interval = Column(Integer(), nullable=False)
    ts = Column(Integer(), nullable=False)
    dt = Column(DateTime(), default=datetime.now)
    open = Column(Float(), nullable=False)
    high = Column(Float(), nullable=False)
    low = Column(Float(), nullable=False)
    close = Column(Float(), nullable=False)
    volume = Column(Float(), nullable=False)


class Symbol(Base):
    __tablename__ = 'symbols'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(100), nullable=False, comment='тип: спот, фьючерс или др')
    exchange_name = Column(String(50), nullable=False, comment='имя биржи, на которой котируется символ')
    dt_begin = Column(DateTime(), default=datetime.now)
    dt_begin_historical = Column(DateTime(), default=datetime.now)


class QuotedSymbol(Base):
    __tablename__ = 'quotedsymbols'
    id = Column(Integer(), primary_key=True)
#    symbol_id --- связи::::


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer(), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    orders = relationship("Order", backref='customer')


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer(), primary_key=True)
    name = Column(String(200), nullable=False)
    cost_price = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer())


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer(), primary_key=True)
    customer_id = Column(Integer(), ForeignKey('customers.id'))
    date_placed = Column(DateTime(), default=datetime.now)
    line_items = relationship("OrderLine", backref='order')


class OrderLine(Base):
    __tablename__ = 'order_lines'
    id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey('orders.id'))
    item_id = Column(Integer(), ForeignKey('items.id'))
    quantity = Column(SmallInteger())
    item = relationship("Item")
