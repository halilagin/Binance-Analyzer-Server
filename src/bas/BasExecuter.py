# -*- coding: utf-8 -*-


'''
Created on Jan 10, 2018

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
import threading
from bas.BasCoinManager import BasCoinManager
from bas.BasMongoManager import BasMongoManager
from bas.BasBinanceClientState import BasClientState
from bas.BasInitializer import BasInitializer
from bas.BasThreadCandleWriter import BasThreadCandleWriter
from bas.BasThreadInitializer import BasThreadInitializer
from bas.BasWebSocket import BasWebSocketServer
from bas.BasThreadCandleReader import BasThreadCandleReader


BasLocks_WebSocketCandleReaderClients=[]
BasLocks_WebSocketCandleReaderClients_lock=threading.Lock()
BasLocks_initializer=threading.Lock()
BasLocks_initializerProgress=0.0

#hash <client id,[threads]> 
BasLocks_ClientThreads={}


class BasExecuter(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        self.params = params  
    
    
    
    def plostTest(self, symbol="XLMETH", interval=Client.KLINE_INTERVAL_1MINUTE):
        pass
        
        
        candles = self.binanceManager.getCandles(symbol=symbol, interval=interval)
        candlesMap = basCandleReader.map(candles)
        candles = np.array(candles,  dtype='f')
        
        time_ = [int(c["openTime"]/1000) for c in candlesMap]
        middle_ = [c["middle"] for c in candlesMap]

        
        print("first,last", time_[0],basTimer.toHMString(time_[0]), basTimer.toHMString(time_[len(time_)-1]) )
        print("first,last,datetime", basTimer.toDateTimeString(time_[0]), basTimer.toDateTimeString(time_[len(time_)-1]) )
        stime = self.binanceManager.getServerTime()
        print ("servertime:", stime, basTimer.toDateTimeString(stime/1000))
        print ("candles.timelong:", math.floor (len(time_)/60), "hour", len(time_)%60, "minutes")


         
        secs = mdate.epoch2num(time_)
        #date_fmt = '%d-%m-%y %H:%M:%S'
        date_fmt = '%H:%M'
         
        fig, ax = plt.subplots()
        ax.plot_date(secs, middle_, "r-")
        date_formatter = mdate.DateFormatter(date_fmt)
        ax.xaxis.set_major_formatter(date_formatter)
        #fig.autofmt_xdate() #Sets the tick labels diagonal so they fit easier.
        plt.show()
    
    def initialize(self):
        BasInitializer({}).start()
    # np.array type conversion : https://docs.scipy.org/doc/numpy-1.13.0/user/basics.types.html
    #epoch time matplotlib :https://stackoverflow.com/questions/23294197/plotting-chart-with-epoch-time-x-axis-using-matplotlib
    
    def initializeThreads(self):
        self.threads={}
        self.threads["candleWriter"] = BasThreadCandleWriter()
        self.threads["candleReaders"] = [] # array of candle readers per plot

        self.threads["initializer"] = BasThreadInitializer()
        
        
        
    def startThreads(self):
        pass
        print("starting the threads")
        self.threads["candleWriter"].start()
        #self.threads["candleReaders"].start()

        
        
    def start(self):
        print ("BasExecuter started!", _bas)
        self.configManager = BasConfigManager(self.params)
        self.configManager.read()
        self.state = BasClientState().state
        
        
        self.binanceManager = BasBinanceManager() 
        self.currencyManager = BasCoinManager()
        self.mongoManager = BasMongoManager()
        self.initializeThreads()
        
        
        
        if _bas.executer.configManager.config.bas.application.firstRun==1: #the application is opened first time
            print ("application is running first time!")
            #self.initialize()
            self.threads["initializer"].start()
        else:
            pass
            self.startThreads()
        
        self.webSocketServer = BasWebSocketServer()
        self.webSocketServer.run()
        
        #self.binanceManager.getRecentTrades("XLMETH")
        
        
        
       
