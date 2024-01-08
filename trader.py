from datafeed import *


class Trader:
    data: TDataFeeder

    def __init__(self, data):
        self.data = data


class JZTrader(Trader):
    pass

