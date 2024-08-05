import configparser
from dataclasses import dataclass
from datetime import *

config = configparser.ConfigParser()
config.read('cfg/settings.ini')

cUp = '#59B359'
cDn = '#D96C6C'
cStream = "#B9A6FF"
cLimit = "FF00FF"
cLtGray = "eeeeee"
cGray = "bbbbbb"


def realdt(s):
    moscow = timezone(timedelta(hours=3), "Moscow")
    return datetime.strptime(s, '%Y-%m-%d').astimezone(datetime.now(moscow).tzinfo)


def begindt():
    return datetime(1979, 7, 28)
