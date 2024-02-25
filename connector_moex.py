# import requests
import requests
from requests.auth import HTTPBasicAuth
from connector import *
import apimoex
import json
from datetime import datetime


class TMOEXConnectorNoAuth(TConnector):
    url_iss = ''
    session = None

    def __init__(self):
        super().__init__('MOEX')
        self.url_iss = config.get('CONNECTOR: MOEX', 'url_iss')

    # def a1(self):
    #     with requests.Session() as session:
    #         data = apimoex.get_board_history(session, 'SNGSP')
    #         df = pd.DataFrame(data)
    #         df.set_index('TRADEDATE', inplace=True)
    #         print(df.head(), '\n')
    #         # print(df.tail(), '\n')
    #         # df.info()


class TMOEXConnector(TMOEXConnectorNoAuth):
    login = ''
    password = ''
    cookies = None
    url_auth = ''
    url_oi = ''

    def __init__(self):
        super().__init__()

        self.login = config.get('CONNECTOR: MOEX', 'login')
        self.password = config.get('CONNECTOR: MOEX', 'password')

        self.session = requests.Session()
        self.session.get(config.get('CONNECTOR: MOEX', 'url_auth'), auth=(self.login, self.password))
        self.headers = {'User-Agent': self.session.headers['User-Agent']}
        self.cookies = {'MicexPasswordCert': self.session.cookies['MicexPassportCert']}
        self.url_oi = config.get('CONNECTOR: MOEX', 'url_oi')

    def get_futures_oi(self, symbol, from_date: datetime = None, to_date: datetime = None):
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

