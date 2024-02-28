# import requests
import requests
from requests.auth import HTTPBasicAuth
from connector import *
import apimoex
import json
from datetime import datetime


class TMOEXConnector(TConnector):
    url_iss = ''
    session = None
    login = ''
    password = ''
    cookies = None
    url_auth = ''
    url_oi = ''

    def __init__(self):
        super().__init__('MOEX')
        self.url_iss = config.get('CONNECTOR: MOEX', 'url_iss')

        self.login = config.get('CONNECTOR: MOEX', 'login')
        self.password = config.get('CONNECTOR: MOEX', 'password')

        self.session = requests.Session()
        self.session.get(config.get('CONNECTOR: MOEX', 'url_auth'), auth=(self.login, self.password))
        self.headers = {'User-Agent': self.session.headers['User-Agent']}
        self.cookies = {'MicexPasswordCert': self.session.cookies['MicexPassportCert']}
        self.url_oi = config.get('CONNECTOR: MOEX', 'url_oi')

    def get_oi(self, symbol, from_date: datetime = None, to_date: datetime = None):
        # fd = from_date.date().strftime('%Y-%m-%d')
        # td = to_date.date().strftime('%Y-%m-%d')
        # print(fd)
        # print(td)

        # r = requests.get(self.url_oi + '/' + symbol + '.json?from='+fd+'&till='+td,
        r = requests.get(self.url_oi + '/' + symbol + '.json?from=2020-05-12&till=2020-05-15',
                         headers=self.headers, cookies=self.cookies)
        js = json.loads(r.content)
        df = DataFrame(js['futoi']['data'], columns=list(js['futoi']['columns']))

        return df

    # def get_spot(self, s):
    #     r = requests.get(config.get('CONNECTOR: MOEX', 'url_securities') + '/' + s)
    #     js = json.loads(r.content)
    #
    #     return spot

    @staticmethod
    def get_info(ticker):
        r = requests.get(config.get('CONNECTOR: MOEX', 'url_securities') + '/' + ticker + '.json')
        return json.loads(r.content)

    @staticmethod
    def convert_interval(interval):
        if interval == 1: return 31

    def get_candles(self, ticker, interval, from2, to2):
        logger.info("moex connector, start getting candles, symbol=" + ticker + ", Interval=" + str(interval) + "...")
        r = apimoex.get_market_candles(self.session, ticker, interval=31)
        print(r)

# worked
# http://iss.moex.com/iss/history/engines/currency/markets/selt/securities/USD000UTSTOM
