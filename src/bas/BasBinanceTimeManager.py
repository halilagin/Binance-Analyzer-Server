'''
Created on Jan 11, 2018

@author: halil
'''
import datetime
import time
import enum




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
    Week = 7 * 24 * 60* 60
    TwoWeek = 2 * 7 * 24 * 60* 60
    Month = 1 * 30 * 24 * 60* 60
    TwoMonth = 2 * 30 * 24 * 60* 60
    ThreeMonth = 3 * 30 * 24 * 60* 60
    SixMonth = 6 * 30 * 24 * 60* 60
    Year= 12 * 30 * 24 * 60* 60

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