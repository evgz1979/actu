import configparser
from datetime import *

config = configparser.ConfigParser()
config.read('cfg/settings.ini')

cUp = '#59B359'
cDn = '#D96C6C'
cStream = "#B9A6FF"


def realdt(s):
    moscow = timezone(timedelta(hours=3), "Moscow")
    return datetime.strptime(s, '%Y-%m-%d').astimezone(datetime.now(moscow).tzinfo)
