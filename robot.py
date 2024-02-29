from symbols import *


class TDataFeeder:
    pass


class TRobot:
    data: TDataFeeder
    connectors = []
    symbols = []
    metas = []  # meta symbols

    #  db = TDataBase
    quoted_by_orm = []
    _quoted_symbol_0 = Symbol

    def _print_0(self):  # temp
        for qs11 in self.quoted_by_orm:
            print('   * quoted symbol: ',
                  qs11.name)  # ,'... please wait while quoted symbol refreshing candles data ...')
            # refresh_quoted_symbol(qs)

    def _load_from_db(self):
        with Session(engine) as session:
            statement = select(Symbol).where(Symbol.quoted)

            results = session.exec(statement)

            for symbol in results:
                self.quoted_by_orm.append(symbol)

            if len(self.quoted_by_orm) == 0:
                print('adding quoted_symbol_0')
                session.add(self._quoted_symbol_0)
                session.commit()

                results = session.exec(statement)

                for symbol in results:
                    self.quoted_by_orm.append(symbol)

    def __init__(self):
        # temp - quoted_symbol_0 - если нет котируемых символов нигде в базе, пока временно используем этот,
        # позже сделать чтобы спрашивал из возможных вариантов
        self._quoted_symbol_0 = Symbol(name='BTC/USDT', exchange_name='kucoin', exchange_section='spot',
                                       dt_analyzer_start_from=datetime.now(), dt_historical_start=datetime.now(),
                                       quoted=True)
        self._load_from_db()

    def find_connector(self, _id):
        for c in self.connectors:
            if c.id == _id: return c

    def main(self):
        for connector in self.connectors:
            connector.main()

        for ms in self.metas:
            print("... meta symbol: " + ms.alias + ' ...')

            # пока тупо все заточено под рубль/долл

            # T0
            b = ms.cfg('spot.T0').split(':')
            moex: TMOEXConnector = self.find_connector(b[0])

            st0 = TSymbol('', b[1], '', spot=True)
            st0.info = moex.get_info(b[1])
            st0.connector = moex
            ms.symbols.append(st0)
            ms.spotT0 = st0
            print('spot_T0 (TOD, today) = ' + ms.spotT0.ticker)

            # T1
            a = ms.cfg('spot.T1').split(':')
            conn = self.find_connector(a[0])

            spots = conn.get_spot(a[1])

            s = TSymbol(spots[0].name, spots[0].ticker, spots[0].figi, spot=True)
            s.quoted = True
            s.first_1min_candle_date = spots[0].first_1min_candle_date
            s.first_1day_candle_date = spots[0].first_1day_candle_date
            ms.spotT1 = s
            print('spot_T1 (TOM, tomorow) = ' + ms.spotT1.ticker)
            s.connector = conn
            ms.symbols.append(s)

            # futures
            futures = conn.get_futures(ms.alias)
            for future in futures:

                fut_s = TSymbol(future.name, future.ticker, future.figi, future=True)
                print(fut_s.ticker)

                fut_s.connector = conn
                ms.symbols.append(fut_s)

            ms.future = ms.find_by_ticker(futures[0].ticker)
            ms.future.quoted = True
            print('current future = ' + ms.future.ticker)

            # print(st0.info['description']['data'])

            # oi
            c = ms.cfg('oi').split(':')
            oi = TSymbol(c[1], '', '')
            oi.connector = moex
            ms.symbols.append(st0)
            ms.oi = oi
            print('OI (open interest) = ' + ms.oi.name)

            ms.main()

        # if self.system: self.system.main()

        # logger.info("starting async data.amain() ...")
        # self.amain()

    def amain(self):  # data.amain() is not async !!! - async only connector.amain() and system.amain()
        pass

        # if self.system: self.system.amain()

        # for connector in self.connectors:
        #     asyncio.run(connector.amain())


def load_from_file(file_name: str):  # temp function --- >>> TCandles
    df = pd.read_csv(file_name,
                     dtype={'date': str, 'time': str,
                            'open': float, 'high': float, 'low': float, 'close': float,
                            'volume': float})
    df['dt'] = pd.to_datetime(df['date'] + df['time'])  # as DateTime
    df.drop('date', axis=1, inplace=True)
    df.drop('time', axis=1, inplace=True)
    df['dt'] = df['dt'].astype(str)  # as str
    df.insert(0, 'ts', 0)
    df['ts'] = df.apply(lambda x: iso2timestamp(x['dt'], format='%Y-%m-%d %H:%M:%S'), axis=1)
    df.drop('dt', axis=1, inplace=True)
    df['ts'] = df['ts'].astype(int)
    # df.set_index('ts')
    df = df.set_index('ts')
    df.insert(0, 'dn', 0)
    df.insert(0, 'up', 0)
    return df

    # config = configparser.ConfigParser()  # -> data
    #
    # config.add_section('CONNECTOR: TINKOFF')
    # config.set('CONNECTOR: TINKOFF', 'token',
    #            '')
    # config.set('CONNECTOR: TINKOFF', 'app_name',
    #            'ACTUaliZator 0.1 by JZ')
    #
    # with open('cfg/settings.ini', 'w') as config_file:
    #     config.write(config_file)
    #
    # config.read('cfg/settings.ini')
    # print(config.get('SYMBOLS', 'meta_symbols')
