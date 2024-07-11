# ACTU@liZator, (c) JZ
from system.jz import JZSystem
from system.volk import *
from robot import *
from connector_tinkoff import *
from connector_moex import *
from trader import MOEXTrader

if __name__ == "__main__":

    si = MetaSymbol('USD/RUB')
    cny = MetaSymbol('CNY/RUB')
    sber = MetaSymbol('SBER')

    jz = JZSystem(TDrawer())
    robot = Robot(jz, MOEXTrader(), [TBankConnector(), MOEXConnector()], [sber, cny])
    robot.main()

    # jz.add_interval(Interval.min5)
    # jz.add_interval(Interval.hour1)
    jz.add_interval(sber, Interval.day1)
    jz.add_interval(cny, Interval.week1)

    jz.main()

    robot.amain()  # start async part of app
