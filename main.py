# ACTU@liZator, (c) JZ

from system_vlk import *
from robot import *
from connector_tinkoff import *
from connector_moex import *
from trader import MOEXTrader

if __name__ == "__main__":

    si = MetaSymbol('USD/RUB')
    sber = MetaSymbol('SBER')

    robot = Robot(MOEXTrader(), [si, sber], [TBankConnector()])  # [si, sber]
    robot.main()

    v = TVlkSystem(sber, TDrawer())
    v.add_interval(Interval.day1)
    v.main()

    robot.amain()  # start async part of app
