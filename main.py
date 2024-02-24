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
    tink = TTinkoffConnector(robot.config)  # todo config --> global
    robot.connectors.append(tink)
    moex = TMOEXConnector(robot.config)
    robot.connectors.append(tink)

    ms1 = TMetaSymbol('USD/RUB', connector=tink, moex=moex, config=robot.config)

    robot.meta_symbols.append(ms1)

    trader = JZTrader()
    robot.main()

    vlk = TVlkSystem(ms1, drawer)
    vlk.main()

    drawer.add_candles(ms1.spot_T0.name+':day1', '', ms1.spot_T0.data.day1)
    vlk.draw()  # пока все на 1 ТФ
    drawer.show()  # пока все на 1 ТФ

    # start async part of app
    robot.amain()


