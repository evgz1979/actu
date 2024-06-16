# ACTU@liZator, (c) JZ

from system_vlk import *
from robot import *
from connector_tinkoff import *
from connector_moex import *
from trader import JZTrader


class MetaSi(MetaSymbol):
    moex: MOEXConnector
    tbank: TBankConnector

    def __init__(self):
        super().__init__('USD/RUB')

    def main(self):
        b = self.cfg('spot.T0').split(':')

        st0 = TSymbol('', b[1], '', spot=True)
        st0.info = self.moex.get_info(b[1])
        st0.connector = self.moex
        self.symbols.append(st0)
        self.spotT0 = st0
        print('spot_T0 (TOD, today) = ' + self.spotT0.ticker)

        a = self.cfg('spot.T1').split(':')

        spots = self.tbank.get_spot(a[1])

        s = TSymbol(spots[0].name, spots[0].ticker, spots[0].figi, spot=True)
        s.quoted = True
        s.first_1min_candle_date = spots[0].first_1min_candle_date
        s.first_1day_candle_date = spots[0].first_1day_candle_date
        self.spotT1 = s
        print('spot_T1 (TOM, tomorow) = ' + m_si.spotT1.ticker)
        s.connector = self.tbank
        self.symbols.append(s)

        # futures
        futures = self.tbank.get_futures(self.alias)
        for future in futures:

            fut_s = TSymbol(future.name, future.ticker, future.figi, future=True)
            print(fut_s.ticker)

            fut_s.connector = self.tbank
            self.symbols.append(fut_s)

        m_si.future = m_si.find_by_ticker(futures[0].ticker)
        m_si.future.quoted = True
        print('current future = ' + self.future.ticker)

        # oi
        c = self.cfg('oi').split(':')
        oi = TSymbol(c[1], '', '')
        oi.connector = self.moex
        self.symbols.append(st0)
        self.oi = oi
        print('OI (open interest) = ' + self.oi.name)

        super().main()


class RobotSi(TRobot):
    meta: MetaSi

    def main(self):
        super().main()
        self.meta = self.metas[0]
        self.meta.tbank = self.connectors.append(TBankConnector())
        self.meta.moex = self.connectors.append(MOEXConnector())

        self.meta.main()  # todo пока так, --> TRobot (сделать всеболее абстрактным)


if __name__ == "__main__":

    m_si = MetaSi()
    robot = RobotSi(JZTrader(), [m_si])
    robot.main()

    drawer = TDrawer()
    p1 = drawer.plots.append(TDrawerPlot(m_si.future.ticker))
    ax01 = p1.add_candles(m_si.future.data.day1)

    vlk = TVlkSystem(m_si, drawer)
    vlk.add_methods(Interval.day1, ax01)
    vlk.main()

    vlk.draw()
    drawer.show()

    robot.amain()  # start async part of app


