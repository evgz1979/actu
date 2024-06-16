# ACTUaliZator, (c) JZ
from drawer import *
from system_vlk import *

from robot import *
from connector_tinkoff import *
from connector_moex import *
from trader import JZTrader


class TRobot1(TRobot):
    moex: TMOEXConnector
    tbank: TTinkoffConnector
    vlk: TVlkSystem

    def main(self):
        super().main()

        self.tbank = self.connectors.append(TTinkoffConnector())
        self.moex = self.connectors.append(TMOEXConnector())

        ms = self.metas[0]  # пока тупо все заточено под рубль/долл

        b = ms.cfg('spot.T0').split(':')

        st0 = TSymbol('', b[1], '', spot=True)
        st0.info = self.moex.get_info(b[1])
        st0.connector = self.moex
        ms.symbols.append(st0)
        ms.spotT0 = st0
        print('spot_T0 (TOD, today) = ' + ms.spotT0.ticker)

        a = ms.cfg('spot.T1').split(':')

        spots = self.tbank.get_spot(a[1])

        s = TSymbol(spots[0].name, spots[0].ticker, spots[0].figi, spot=True)
        s.quoted = True
        s.first_1min_candle_date = spots[0].first_1min_candle_date
        s.first_1day_candle_date = spots[0].first_1day_candle_date
        ms.spotT1 = s
        print('spot_T1 (TOM, tomorow) = ' + ms.spotT1.ticker)
        s.connector = self.tbank
        ms.symbols.append(s)

        # futures
        futures = self.tbank.get_futures(ms.alias)
        for future in futures:

            fut_s = TSymbol(future.name, future.ticker, future.figi, future=True)
            print(fut_s.ticker)

            fut_s.connector = self.tbank
            ms.symbols.append(fut_s)

        ms.future = ms.find_by_ticker(futures[0].ticker)
        ms.future.quoted = True
        print('current future = ' + ms.future.ticker)

        # oi
        c = ms.cfg('oi').split(':')
        oi = TSymbol(c[1], '', '')
        oi.connector = self.moex
        ms.symbols.append(st0)
        ms.oi = oi
        print('OI (open interest) = ' + ms.oi.name)

        robot.metas[0].main()  # todo пока так, --> TRobot (сделать всеболее абстрактным)

        p1 = self.drawer.plots.append(TDrawerPlot(ms.future.ticker))
        ax01 = p1.add_candles(ms.future.data.day1)

        self.vlk = TVlkSystem(ms, self.drawer)
        self.vlk.add_methods(Interval.day1, ax01)
        self.vlk.main()

        self.vlk.draw()
        self.drawer.show()


if __name__ == "__main__":

    robot = TRobot1(JZTrader(), TDrawer(), [TMetaSymbol('USD/RUB')])
    robot.main()
    robot.amain()  # start async part of app


