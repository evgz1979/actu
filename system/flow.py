from system.abstract import *


class TFlowMethod(TAnalysisMethod):
    id = 'FLOW'


class TTreeFlowMethod(TAnalysisMethod):
    id = 'TREE-FLOW'

    # data: tree


class TFlowDonwgradeMethod(TFlowMethod):
    id = 'DOWNGRADEFLOW'
