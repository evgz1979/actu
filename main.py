# ACTUaliZator, (c) JZ

from drawer import *
from system_volk import *
from trader import *
from robot import *
from connector_tinkoff import *
# import yfinance as yf
# import finplot as fplt


if __name__ == "__main__":

    robot = TRobot()
    c_tink = TTinkoffConnector(robot.config)
    robot.connectors.append(c_tink)
    ms1 = TMetaSymbol('USD/RUB', c_tink, robot.config)
    robot.meta_symbols.append(ms1)
    trader = JZTrader(robot)

    robot.main(TVolkSystem(ms1))  # -> robot.main(data, system, trader, drawer) -- later !

    drawer = TDrawer()
    drawer.append(ms1.spot_T0.name+':day1', ms1.spot_T0.data.day1)
    drawer.show()

    robot.amain()  # start async part of app


# data = [(instrument, yf.download(instrument, '2020-10-01')) for instrument in ('AAPL','GOOG','TSLA')]
#
# for i,(instrument_a,dfa) in enumerate(data):
#
#     for instrument_b,dfb in data[i+1:]:
#
#         ax = fplt.create_plot(instrument_a+' vs. '+instrument_b+' (green/brown)', maximize=False)
#         dfa['Open Close High Low'.split()].plot(kind='candle', ax=ax)
#         pb = dfb['Open Close High Low'.split()].plot(kind='candle', ax=ax.overlay(scale=1.0))
#         pb.colors['bull_body'] = '#0f0'
#         pb.colors['bear_body'] = '#630'
# fplt.show()
