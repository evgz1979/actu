from datafeeder import TDataFeeder
from symbols import *
from system.abstract import AnalysisSystem


class Robot:
    data: TDataFeeder
    connectors = TConnectors
    metas = MetaSymbols
    system = AnalysisSystem

    def __init__(self, system: AnalysisSystem, _connectors: [TConnector], _metas: [MetaSymbol]):

        self.system = system
        self.system.metas = _metas

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


