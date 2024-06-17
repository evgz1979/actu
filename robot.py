from datafeeder import TDataFeeder
from symbols import *
from trader import Trader


class Robot:
    data: TDataFeeder
    connectors = TConnectors
    metas = TMetaSymbols
    trader = Trader

    def __init__(self, trader: Trader, _metas: [MetaSymbol], _connectors: [TConnector]):

        self.trader = trader

        self.connectors = TConnectors()
        self.metas = TMetaSymbols(self.connectors)

        for ms in _metas:
            self.metas.append(ms)

        for c in _connectors:
            self.connectors.append(c)

    def main(self):
        self.connectors.main()
        self.metas.main()

    def amain(self):
        pass


