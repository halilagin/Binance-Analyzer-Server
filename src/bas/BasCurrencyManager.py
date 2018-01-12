'''
Created on Jan 11, 2018

@author: halil
'''
import yaml
import io
from bas.BasBinanceManager import BasBinanceManager
from bas.BasConfigManager import BasConfigManager
from  bas.BasContext import _bas 
from binance.client import Client
from bas.BasBinanceCandleReader import basCandleReader
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import datetime
from bas.BasBinanceTimeManager import basTimer
import math

from bas.BasContext import _bas

class BasCurrencyManager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    
    def fetchCandleTest(self, symbol="XLMETH", interval=Client.KLINE_INTERVAL_1MINUTE):
        pass
        
        
        candles = self.binanceManager.getCandles(symbol=symbol, interval=interval)
        candlesMap = basCR.map(candles)
        candles = np.array(candles,  dtype='f')
        
        time_ = [int(c["openTime"]/1000) for c in candlesMap]
        middle_ = [c["middle"] for c in candlesMap]

        
        print("first,last", time_[0],basTimer.toHMString(time_[0]), basTimer.toHMString(time_[len(time_)-1]) )
        print("first,last,datetime", basTimer.toDateTimeString(time_[0]), basTimer.toDateTimeString(time_[len(time_)-1]) )
        stime = self.binanceManager.getServerTime()
        print ("servertime:", stime, basTimer.toDateTimeString(stime/1000))
        print ("candles.timelong:", math.floor (len(time_)/60), "hour", len(time_)%60, "minutes")


         
#         secs = mdate.epoch2num(time_)
#         #date_fmt = '%d-%m-%y %H:%M:%S'
#         date_fmt = '%H:%M'
#          
#         fig, ax = plt.subplots()
#         ax.plot_date(secs, middle_, "r-")
#         date_formatter = mdate.DateFormatter(date_fmt)
#         ax.xaxis.set_major_formatter(date_formatter)
#         #fig.autofmt_xdate() #Sets the tick labels diagonal so they fit easier.
#         plt.show()
    
    
    
    def fetchCandle(self, symbol="XLMETH", interval=Client.KLINE_INTERVAL_1MINUTE):
        pass
        
        
        candles = _bas.executer.binanceManager.getCandles(symbol=symbol, interval=interval)
        candlesMap = basCandleReader.map(candles,interval)
        candles = np.array(candles,  dtype='f')
        
        time_ = [int(c["openTime"]/1000) for c in candlesMap]
        middle_ = [c["middle"] for c in candlesMap]
        
        return {"candleMiddle":middle_, "time":time_}
    