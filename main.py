# ACTUaliZator, (c) JZ
from drawer import *
from system_vlk import *
from trader import *
from robot import *
from connector_tinkoff import *
from connector_moex import *


if __name__ == "__main__":

    robot = TRobot()
    drawer = TDrawer()
    p1 = drawer.plots.append(TDrawerPlot('1d: usd/rub', 3))
    p2 = drawer.plots.append(TDrawerPlot('1h: usd/rub', 2))

    robot.connectors.append(TTinkoffConnector())
    robot.connectors.append(TMOEXConnector())
    robot.metas.append(TMetaSymbol('USD/RUB'))

    trader = JZTrader()
    robot.main()

    # todo -- drawer schema
    ax01 = drawer.plots[0].add_candles(robot.metas[0].spotT1.data.day1, 0)
    drawer.plots[0].add_candles(robot.metas[0].spotT1.data.day1, 1)  # todo st0 !!! from MOEX
    drawer.plots[0].add_candles(robot.metas[0].future.data.day1, 2)

    ax02 = drawer.plots[1].add_candles(robot.metas[0].spotT1.data.hour1, 0)
    drawer.plots[1].add_candles(robot.metas[0].spotT1.data.hour1, 1)

    vlk = TVlkSystem(robot.metas[0], drawer)
    vlk.add_methods(Interval.day1, ax01)
    vlk.add_methods(Interval.hour1, ax02)
    vlk.main()

    vlk.draw()
    drawer.show()

    robot.amain()  # start async part of app


