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
    drawer.plots.append(TDrawerPlot('usd/rub', 3))
    # drawer.plots.append(TDrawerPlot('si', 1))

    robot.connectors.append(TTinkoffConnector())
    robot.connectors.append(TMOEXConnector())
    robot.metas.append(TMetaSymbol('USD/RUB'))

    trader = JZTrader()
    robot.main()

    vlk = TVlkSystem(robot.metas[0], drawer)
    vlk.main()

    a0 = drawer.plots[0].add_candles(robot.metas[0].sT1.data.day1, 0)
    a1 = drawer.plots[0].add_candles(robot.metas[0].sT1.data.day1, 1)  # todo st0 !!! from MOEX
    a2 = drawer.plots[0].add_candles(robot.metas[0].future.data.day1, 2)

    vlk.draw()
    drawer.show()

    robot.amain()  # start async part of app


