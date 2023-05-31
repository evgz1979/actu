from peewee import *

db_path01 = 'db/BTCUSDT.db'
db = SqliteDatabase(db_path01)


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db


class Symbol(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'symbols'


class Candle(BaseModel):
    interval = IntegerField()
    dt = DateTimeField()
    open = FloatField()
    high = FloatField()
    low = FloatField()
    close = FloatField()
    volume = FloatField()

    class Meta:
        db_table = 'candles'


def db_create():
    db.create_tables([Candle])


def select_test1():
    query = Candle.select().where(Candle.interval == 1)

    for p in query:
        print(p.open)
