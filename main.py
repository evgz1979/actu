# ACTU@liZator, (c) JZ

from system.volk import *
from robot import *
from connector_tinkoff import *
from connector_moex import *
from trader import MOEXTrader

if __name__ == "__main__":

    si = MetaSymbol('USD/RUB')
    sber = MetaSymbol('SBER')

    robot = Robot(MOEXTrader(), [si, sber], [TBankConnector(), MOEXConnector()])  # [si, sber]
    robot.main()

    v = VolkSystem(sber, TDrawer())
    v.add_interval(Interval.day1)
    v.main()

    robot.amain()  # start async part of app
