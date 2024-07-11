from datafeeder import TDataFeeder
from symbols import *
from system.abstract import AnalysisSystem
from trader import Trader


class Robot:
    data: TDataFeeder
    connectors = TConnectors
    metas = MetaSymbols
    trader = Trader
    system = AnalysisSystem

    def __init__(self, system: AnalysisSystem, trader: Trader, _connectors: [TConnector], _metas: [MetaSymbol]):

        self.system = system
        self.system.metas = _metas

        self.trader = trader

        self.connectors = TConnectors()
        self.metas = MetaSymbols(self.connectors)

        for ms in _metas:
            self.metas.append(ms)

        for c in _connectors:
            self.connectors.append(c)

    def main(self):
        self.connectors.main()
        self.metas.main()

    def amain(self):
        pass


