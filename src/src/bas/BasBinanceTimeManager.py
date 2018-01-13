'''
Created on Jan 11, 2018

@author: halil
'''
import datetime
import time
import enum
from binance.client import Client




# see : https://docs.python.org/3/library/enum.html
class BasBinanceTimeInterval(enum.Enum):
    #in seconds
    OneMinute=60
    FiveMinute= 5 * 60
    TenMinute= 10 * 60
    FifteenMinute= 15 * 60
    ThirtyMinute= 30 * 60
    OneHour= 60* 60
    TwoHour= 2 * 60* 60
    FourHour= 4 * 60* 60
    SixHour= 6 * 60* 60
    EightHour= 8 * 60* 60
    TwelveHour= 12 * 60* 60
    OneDay = 1 * 24 * 60* 60
    TwoDay = 2 * 24 * 60* 60
    ThreeDay = 3 * 24 * 60* 60
    OneWeek = 7 * 24 * 60* 60
    TwoWeek = 2 * 7 * 24 * 60* 60
    OneMonth = 1 * 30 * 24 * 60* 60
    TwoMonth = 2 * 30 * 24 * 60* 60
    ThreeMonth = 3 * 30 * 24 * 60* 60
    SixMonth = 6 * 30 * 24 * 60* 60
    oneYear= 1 * 12 * 30 * 24 * 60* 60

class BinanceTimeIntervalWrapper(object):
    pass
    def __init__(self):
        pass
    
    def kline(self, timeInterval):
        if timeInterval==BasBinanceTimeInterval.OneMinute.value:
            return Client.KLINE_INTERVAL_1MINUTE
        elif timeInterval==BasBinanceTimeInterval.FiveMinute.value:
            return Client.KLINE_INTERVAL_5MINUTE
        elif timeInterval==BasBinanceTimeInterval.FifteenMinute.value:
            return Client.KLINE_INTERVAL_15MINUTE
        elif timeInterval==BasBinanceTimeInterval.ThirtyMinute.value:
            return Client.KLINE_INTERVAL_30MINUTE
        elif timeInterval==BasBinanceTimeInterval.OneHour.value:
            return Client.KLINE_INTERVAL_1HOUR
        elif timeInterval==BasBinanceTimeInterval.TwoHour.value:
            return Client.KLINE_INTERVAL_2HOUR
        elif timeInterval==BasBinanceTimeInterval.FourHour.value:
            return Client.KLINE_INTERVAL_4HOUR
        elif timeInterval==BasBinanceTimeInterval.SixHour.value:
            return Client.KLINE_INTERVAL_6HOUR
        elif timeInterval==BasBinanceTimeInterval.EightHour.value:
            return Client.KLINE_INTERVAL_8HOUR
        elif timeInterval==BasBinanceTimeInterval.TwelveHour.value:
            return Client.KLINE_INTERVAL_12HOUR
        elif timeInterval==BasBinanceTimeInterval.OneDay.value:
            return Client.KLINE_INTERVAL_1DAY
        elif timeInterval==BasBinanceTimeInterval.OneWeek.value:
            return Client.KLINE_INTERVAL_1WEEK
        elif timeInterval==BasBinanceTimeInterval.OneMonth.value:
            return Client.KLINE_INTERVAL_1MONTH
        
        return Client.KLINE_INTERVAL_1MINUTE
        
basTimeintervalWrapper = BinanceTimeIntervalWrapper()        

class BasBinanceTimeManager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def nowInMillisecond(self):
        return int(time.time()*1000)
    
    def nowInMicrosecond(self):
        return int(time.time()*1000000)
        
    def toSec(self, epoch):
        return epoch/60000
    
    def toHMString(self,epoch):
        return datetime.datetime.fromtimestamp(epoch).strftime('%H:%M')
        

    def toDateTimeString(self,epoch):
        return datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S.%f')
        


basTimer = BasBinanceTimeManager() 
