# ACTU@liZator, (c) JZ
from system.jz import JZSystem
from robot import *
from connector.tbank import *
from connector.moex import *
from connector.kucoin import *
from drawer import *

if __name__ == "__main__":

    # si = MetaSymbol('USD/RUB')
    # cny = MetaSymbol('CNY/RUB')
    sber = MetaSymbol('SBER')

    jz = JZSystem(TDrawer())

    cTBank = TBankConnector()
    # cMOEX = MOEXConnector()

    # cKuCoin = KUCoinConnector()
    # df = cKuCoin.get_candles_df('BTC/USDT', '1m')
    # print(df)

    # robot = Robot(jz, [cTBank, cMOEX], [sber, cny])
    robot = Robot(jz, [cTBank], [sber])
    robot.main()

    jz.add_interval(sber, Interval.day1)

    jz.main()

    robot.amain()  # start async part of app
