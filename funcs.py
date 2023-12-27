import datetime
import logging

import pytz

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def cast_money(v):
    """
    https://tinkoff.github.io/investAPI/faq_custom_types/
    :param v:
    :return:
    """
    return v.units + v.nano / 1e9  # nano - 9 нулей


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