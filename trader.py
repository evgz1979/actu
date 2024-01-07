from datafeed import *


class Trader:
    data: TDataFeeder

    def __init__(self, data):
        self.data = data


class VolkTrader(Trader):
    pass


class JZTrader(Trader):
    pass

