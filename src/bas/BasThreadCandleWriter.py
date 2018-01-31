'''
Created on Jan 12, 2018

@author: halil
'''
import time
import threading
from bas.BasContext import _bas
from bas.BasBinanceTimeManager import basTimer, BasBinanceTimeInterval,\
    basTimeintervalWrapper
from bas.BasBinanceCandleReader import basCandleReader
from bas.BasCoinManager import basCoinmanager
from bas.BasBinanceClientState import BasThreadState



#see: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html

class BasThreadCandleWriter(threading.Thread):
    
        
        def __init__(self, threadID="BasThreadCandleWriter",params={}, name=None):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.state = BasThreadState.FirstRun
            
            #params:{symbol:limit,tiemInterval}
            self.params = params
            self.symbol=None
            self.limit=None
            self.timeInterval=None
            
            if "symbol" in self.params:
                self.symbol = self.params["symbol"]
            if "limit" in self.params:
                self.limit = self.params["limit"]
            if "timeInterval" in self.params:
                self.timeInterval = self.params["timeInterval"]
            
            self.mostRecentCandle=None
            
        
        
        def saveCandleDocs(self, timeInterval):
            if len(self.candleDocs)==0:
                return
            print("[CandleWriter] [saved.candles.count]",len(self.candleDocs))
            _bas.executer.mongoManager.saveUpdateCollection(_bas.executer.mongoManager.candles,self.candleDocs)
            
        def saveCandles(self, candles, timeInterval, symbol):
            if len(candles)==0:
                return
            self.candleDocs = basCandleReader.mapMongoDoc(candles, timeInterval, symbol)
            self.saveCandleDocs(timeInterval)
            
            
         
        def doWork(self):
            #self.signal.emit({"action":"candleTracker", "data":self.candles, "params":self.params})
            if self.mostRecentCandle==None:
                #print("[CandleWriter] [first time running. grab]", self.limit)
                self.candles = _bas.executer.binanceManager.getCandles(
                symbol=self.symbol, 
                interval= basTimeintervalWrapper.kline(self.timeInterval), 
                limit=self.limit 
                #startTime=int(self.lastCandleInMongoDB["openTime"])
                )
                
            else:
                #print("[CandleWriter] [grap candles starting from most recent candle]", self.mostRecentCandle["openTime"]*1000)
                self.candles = _bas.executer.binanceManager.getCandles(
                symbol=self.symbol, 
                interval= basTimeintervalWrapper.kline(self.timeInterval), 
                limit=self.limit, 
                startTime=int(self.mostRecentCandle["openTime"]*1000) ##saved after dividing 1000, then restore the original back and request.
                )
            #print("[CandleWriter] [Binance recevied candle count]", len(self.candles))
            if len(self.candles)>0:
                self.candleDocs = basCandleReader.mapMongoDoc(self.candles,self.timeInterval, self.symbol)
                a = self.candleDocs[-1]
                self.mostRecentCandle = basCandleReader.copyDoc(a)
                self.saveCandleDocs(self.timeInterval)
            #self.saveCandles(self.candles, self.timeInterval)
            self.candles = None
            self.candleDocs = None
        def run(self):
            self.waitTime = _bas.executer.configManager.config.bas.threads.candleWriter.waitTime
            if self.state.value==BasThreadState.FirstRun.value:
                if self.symbol==None or self.symbol not in basCoinmanager.coinSymbols:
                    self.symbol = _bas.executer.configManager.config.bas.default.trade.symbol
                if self.limit==None or self.limit <5 or self.limit>500:
                    self.limit= _bas.executer.configManager.config.bas.threads.candleWriter.limit
                if self.timeInterval==None or self.timeInterval< BasBinanceTimeInterval.OneMinute or self.timeInterval>BasBinanceTimeInterval.oneYear:
                    self.timeInterval= _bas.executer.configManager.config.bas.default.trade.timeInterval
        
                #fetchCount = _bas.executer.state.candleTracker.maxFetchCount
                #self.candles = _bas.executer.binanceManager.getCandles(symbol=self.symbol, interval= basTimeintervalWrapper.kline(self.timeInterval), limit=self.limit)
                self.state = BasThreadState.Running.value
#                 self.candleDocs = basCandleReader.mapMongoDoc(self.candles,self.timeInterval, self.symbol)
#                 if len(self.candleDocs)>0:
#                     a = self.candleDocs[-1]
#                     self.mostRecentCandle = basCandleReader.copyDoc(a)
#                     self.saveCandles(self.candles, self.timeInterval, self.symbol)
                
            
            
            while True:
                time.sleep(self.waitTime)
                self.doWork()

