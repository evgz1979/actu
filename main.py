# ACTUaliZator, (c) JZ

from drawer import *
from system_vlk import *
from trader import *
from robot import *
from connector_tinkoff import *
from connector_moex import *
# import yfinance as yf
# import finplot as fplt


if __name__ == "__main__":

    robot = TRobot()
    drawer = TDrawer()

    robot.connectors.append(TTinkoffConnector())
    robot.connectors.append(TMOEXConnector())
    robot.metas.append(TMetaSymbol('USD/RUB'))

    trader = JZTrader()
    robot.main()

    vlk = TVlkSystem(robot.metas[0], drawer)
    vlk.main()

    drawer.add_candles(robot.metas[0].spot_T1.name+':day1', '', robot.metas[0].spot_T1.data.day1)
    # drawer.add_candles(ms1.spot_T1.name+':day1', '', ms1.spot_T1.data.day1)

    vlk.draw()
    drawer.show()

    # start async part of app
    robot.amain()


