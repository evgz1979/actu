from datafeeder import TDataFeeder
from symbols import *
from trader import Trader


class TRobot:
    data: TDataFeeder
    connectors = TConnectors
    metas = TMetaSymbols
    trader = Trader
    drawer = TDrawer

    def __init__(self, trader: Trader, drawer: TDrawer, _metas: [TMetaSymbol]):
        self.metas = TMetaSymbols()
        self.trader = trader
        self.drawer = drawer

        self.connectors = TConnectors()

        for ms in _metas:
            self.metas.append(ms)

    def main(self, ):
        self.connectors.main()

    def amain(self):
        pass


