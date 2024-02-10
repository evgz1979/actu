# ACTUaliZator, (c) JZ

from drawer import *
from system_vlk import *
from trader import *
from robot import *
from connector_tinkoff import *
# import yfinance as yf
# import finplot as fplt


if __name__ == "__main__":

    robot = TRobot()
    drawer = TDrawer()
    c_tink = TTinkoffConnector(robot.config)
    robot.connectors.append(c_tink)
    ms1 = TMetaSymbol('USD/RUB', c_tink, robot.config)
    robot.meta_symbols.append(ms1)
    trader = JZTrader()
    robot.main()

    volk = TVlkSystem(ms1, drawer)
    volk.main()

    drawer.add_candles(ms1.spot_T0.name+':day1', '', ms1.spot_T0.data.day1)
    volk.draw()  # пока все на 1 ТФ
    drawer.show()  # пока все на 1 ТФ

    # start async part of app
    robot.amain()


