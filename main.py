# ACTU@liZator, (c) JZ
from system.jz import JZSystem
from system.volk import *
from robot import *
from connector_tinkoff import *
from connector_moex import *
from trader import MOEXTrader

if __name__ == "__main__":

    si = MetaSymbol('USD/RUB')
    sber = MetaSymbol('SBER')

    robot = Robot(MOEXTrader(), [sber], [TBankConnector(), MOEXConnector()])  # [si, sber]
    robot.main()

    # volk = VolkSystem(sber, TDrawer())
    # volk.add_interval(Interval.day1)
    # volk.main()

    jz = JZSystem(sber, TDrawer())
    jz.add_interval(Interval.day1)
    # jz.add_interval(Interval.week1)
    jz.main()

    robot.amain()  # start async part of app
