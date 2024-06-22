# ACTU@liZator, (c) JZ

from system_vlk import *
from robot import *
from connector_tinkoff import *
from connector_moex import *
from trader import MOEXTrader


if __name__ == "__main__":

    si = MetaSymbol('USD/RUB')
    sber = MetaSymbol('SBER')
    robot = Robot(MOEXTrader(), [si, sber], [TBankConnector(), MOEXConnector()])
    robot.main()

    vlk = TVlkSystem(sber.future, TDrawer())
    vlk.add_interval(Interval.day1)
    vlk.main()
    vlk.draw()

    robot.amain()  # start async part of app

