import ccxt
import datetime
import pytz

key = "VGBlKCHW0Thc0Qk63JvO2FE8Z7lDQpxxlriqgGR1g8ED5OdFgINLqrilvYvlCnze"
secret = "CjDOaNifYTCb7a2KmvGkAFtFOMKDy9dd3psflBzSlyek9rht0Xt1WRup37kxujtO"
symbol_name_bi = 'BTCUSDT'
symbol_name_ku = 'BTC/USDT' #{'spot': 'BTC/USDT', 'futures': 'BTC/USDT:USDT'}




kus = ccxt.kucoin({
    'enableRateLimit': True,
    'apiKey': '63923a46cc568b0001280c4f',
    'secret': 'c2bdd050-252f-4760-b663-a9fe1e6f8162',
    'password': 'vEcnab-wicbot-3gazga'})

kuf = ccxt.kucoinfutures({
    'enableRateLimit': True,
    'apiKey': '63923f2ba0afa6000112b79c',
    'secret': 'bf5dba3b-6af3-40ee-a833-9c35827fff3b',
    'password': 'api_nizwuv-rirWev-gepde9'})

kus.load_markets()
kuf.load_markets({'future': True})

#time.sleep(ku_s.rateLimit / 1000)

#bis = ccxt.binance({'apiKey': 'VGBlKCHW0Thc0Qk63JvO2FE8Z7lDQpxxlriqgGR1g8ED5OdFgINLqrilvYvlCnze',
#                  'secret': 'CjDOaNifYTCb7a2KmvGkAFtFOMKDy9dd3psflBzSlyek9rht0Xt1WRup37kxujtO'})
#bis.load_markets()






def timestamp2iso(timestamp,format='%Y-%m-%dT%H:%M:%S.%fZ'):
    """
    Timestamp transition to ISO8601 standard time (support microsecond output YYYY-MM-DD HH: mm: ss.mmmmmm)

         : param TimeStamp: Timestamp, support seconds, milliseconds, microsecond level

         : param Format: Output time format default ISO =% Y-% M-% DT% H:% M:% S.% FZ; where% f indicates microsecond 6 length

         This function is specially processed, and the millisecond / microsecond portion allows it to support the character format of this part.

    :return:

    """
    format = format.replace('%f','{-FF-}')#
    length = min(16, len(str(timestamp)))# Up to going to microsecond level
    # Get millisecond / microsecond data
    sec = '0'
    if length != 10:#
        sec = str(timestamp)[:16][-(length - 10):]#Gest intercept 16-bit length and then take the last millisecond / microsecond data

        # sec = '{: 0 <6}'. Format (SEC) # long bit 6, relying on the left with 0
        sec = '{:0<3}'.format(sec)  #     3

        timestamp = float(str(timestamp)[:10])# Convert to second timestamp

    return datetime.datetime.utcfromtimestamp(timestamp).strftime(format).replace('{-FF-}',sec)


def iso2timestamp(datestring, format='%Y-%m-%dT%H:%M:%S.%fZ',timespec='milliseconds'):
    """
         ISO8601 time conversion to timestamp

         : param datestring: ISO time string 2019-03-25T16: 00:00.000z, 2019-03-25T16: 00.000111Z
         : Param Format:% Y-% M-% DT% H:% M:% S.% FZ; where% f represents milliseconds or microseconds
         : param Timespec: Return Time Stamp Minimal Unit Seconds Second, MilliseConds Mixi, Microseconds
         : return: Timestamp Default Unit Second
    """
    tz = pytz.timezone('Asia/Shanghai')

    utc_time = datetime.datetime.strptime(datestring, format)  # Read the string to time Class DateTime.DateTime
    time = utc_time.replace(tzinfo=pytz.utc).astimezone(tz)


    times = {
        'seconds': int(time.timestamp()),
        'milliseconds': round(time.timestamp() * 1000),
        'microseconds': round(time.timestamp() * 1000 * 1000),
    }

    return times[timespec]
