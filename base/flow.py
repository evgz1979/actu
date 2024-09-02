from base.stream import *
from settings import *


class FlowPoint:
    si: StreamItem = None
    enlarge = False
    index: int = 0
    up: bool
    # range: int = 0
    # breakp: int = 0
    # prev: 'TTendencyPoint'  # break point

    def __init__(self, stream_item: StreamItem, index, _range=0, prev=None, enlarge=False, up=True):
        self.si = stream_item
        self.index = index
        # self.prev = prev
        self.range = _range
        self.enlarge = enlarge
        self.up = stream_item.up

    def coord(self, delta=0, value=0):
        if value != 0:
            v = value
        else:
            v = self.si.enter[1]
        return self.si.enter[0] + delta, v

    def title(self):
        return str(self.index)
        # return '' if self.index == 1 else str(self.index)

    @property
    def value(self):
        return self.si.value

    @property
    def color(self):
        return cUp if self.up else cDn


class FlowPoints(list[FlowPoint]):
    pass


class SimpleFlow(FlowPoints):
    breakp: FlowPoint = None  # break point
    frsi: FlowPoint = None  # first result stream index
    enter: FlowPoint
    exit: FlowPoint
    index: int

    def __init__(self, range_index=1):
        super().__init__()
        self.index = range_index

    def append(self, __object: FlowPoint) -> FlowPoint:
        super().append(__object)
        return __object

    def start(self, si0, si1: StreamItem):  # start 2 point
        self.breakp = self.frsi = self.enter = self.append(FlowPoint(si0, 1))
        self.exit = self.append(FlowPoint(si1, 2))
        self.exit.up = si0.up
        return self.exit

    def add1p(self, si: StreamItem, index=0):  # add 1 point
        self.exit = self.append(FlowPoint(si, index + 1))
        return self.exit

    def add2p(self, si0, si1: StreamItem, index=0):  # add 2 point
        self.frsi = self.append(FlowPoint(si0, index + 1))
        self.exit = self.append(FlowPoint(si1, index + 2))
        self.exit.up = si0.up
        return self.exit

    @property
    def current(self):
        return self[-1]

    @property
    def prev(self):
        return self[-2]

    def between_last2p(self, si: StreamItem):
        p2 = self.current
        p1 = self.prev
        if p1.up:
            return p2.si.enter[1] >= si.enter[1] >= p1.si.enter[1]
        else:
            return p2.si.enter[1] <= si.enter[1] <= p1.si.enter[1]


class SimpleFlowList(list[SimpleFlow]):
    def append(self, __object: SimpleFlow) -> SimpleFlow:
        super().append(__object)
        return __object


class FlowRanges(SimpleFlowList):

    flow: 'Flow' = None

    @property
    def current(self):
        return self[-1]

    @property
    def prev(self):
        return self[-2]


class Flow:
    current_index: int = 0

    ranges: FlowRanges = None

    @property
    def range(self):
        if self.current_index == 0: return self.ranges[-1]  # current range
        else: return self.ranges[self.current_index - 1]  # for debug

    @property
    def begin(self):
        return self.range[0]

    def __init__(self):
        self.ranges = FlowRanges()

    def start(self, si0, si1: StreamItem):  # start - конкретно для тенденции (а не для Flow)
        self.ranges.append(SimpleFlow())
        return self.range.start(si0, si1)


class Tendency(Flow):

    def union(self, ep: FlowPoint, si: StreamItem):
        p1 = self.begin  # p1 присовить до self.ranges.append() !!!
        self.ranges.append(SimpleFlow(self.range.index+1))
        # return self.range.add1p(si, 2)  # ---- недобавлять 3ю точку!!! union() только объединяет
        # ep.up = not self.begin.up
        p2 = self.range.start(p1.si, ep.si)  # это p2
        p2.up = not self.begin.up
        p2.enlarge = True
        self.range.frsi = p2
        return p2

    def between(self, si: StreamItem):
        if len(self.ranges) == 1:
            p2 = self.range.current
            p1 = self.range.prev
        else:
            p2 = self.range.current
            p1 = self.ranges.prev.frsi

        if p1.up:
            return p2.si.enter[1] >= si.enter[1] >= p1.si.enter[1]
        else:
            return p2.si.enter[1] <= si.enter[1] <= p1.si.enter[1]
