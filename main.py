# ACTU@liZator, (c) JZ

from system_vlk import *
from robot import *
from connector_tinkoff import *
from connector_moex import *
from trader import MOEXTrader


if __name__ == "__main__":

    si = MetaSymbol('USD/RUB')
    # robot = RobotSi(MOEXTrader(), [MetaSymbol('USD/RUB')])
    robot = Robot(MOEXTrader(), [si], [TBankConnector(), MOEXConnector()])
    robot.main()

    drawer = TDrawer()
    p1 = drawer.plots.append(TDrawerPlot(si.future.ticker))
    ax01 = p1.add_candles(si.future.data.day1)

    vlk = TVlkSystem(si, drawer)
    vlk.add_methods(Interval.day1, ax01)
    vlk.main()

    vlk.draw()
    drawer.show()

    robot.amain()  # start async part of app


