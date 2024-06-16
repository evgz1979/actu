# ACTU@liZator, (c) JZ

from system_vlk import *
from robot import *
from connector_tinkoff import *
from connector_moex import *
from trader import JZTrader


class RobotSi(TRobot):
    si: MetaSymbol
    moex: MOEXConnector
    tbank: TBankConnector

    def main(self):
        super().main()

        self.si = self.metas[0]
        self.tbank = self.connectors.append(TBankConnector())
        self.moex = self.connectors.append(MOEXConnector())

        # spot T0
        self.si.spotT0 = self.si.symbols.append(Symbol('', self.si.cfg_ticker('spot.T0'), '', self.moex, spot=True))
        print('spot_T0 (TOD, today) = ' + self.si.spotT0.ticker)

        # spot T1
        spot = self.tbank.get_spot(self.si.cfg_ticker('spot.T1'))
        self.si.spotT1 = self.si.symbols.append(
            Symbol(spot.name, spot.ticker, spot.figi, self.tbank, spot=True, quoted=True,
                   first_1min_candle_date=spot.first_1min_candle_date,
                   first_1day_candle_date=spot.first_1day_candle_date))
        print('spot_T1 (TOM, tomorow) = ' + self.si.spotT1.ticker)

        # futures
        futures = self.tbank.get_futures(self.si.alias)
        for future in futures:
            fut_s = self.si.symbols.append(Symbol(future.name, future.ticker, future.figi, self.tbank, future=True))
            print(fut_s.ticker)

        self.si.future = self.si.find_by_ticker(futures[0].ticker)
        self.si.future.quoted = True
        print('current future = ' + self.si.future.ticker)

        # open interest
        self.si.oi = oi = self.si.symbols.append(Symbol('', self.si.cfg_ticker('oi'), '', self.moex))
        print('OI (open interest) = ' + self.si.oi.name)

        self.si.main()  # todo пока так, --> TRobot (сделать всеболее абстрактным)


if __name__ == "__main__":

    robot = RobotSi(JZTrader(), [MetaSymbol('USD/RUB')])
    robot.main()

    drawer = TDrawer()
    p1 = drawer.plots.append(TDrawerPlot(robot.si.future.ticker))
    ax01 = p1.add_candles(robot.si.future.data.day1)

    vlk = TVlkSystem(robot.si, drawer)
    vlk.add_methods(Interval.day1, ax01)
    vlk.main()

    vlk.draw()
    drawer.show()

    robot.amain()  # start async part of app


