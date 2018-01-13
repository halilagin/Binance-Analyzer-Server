'''
Created on Jan 12, 2018

@author: halil
'''
from PyQt5.Qt import QThread
import time
from bas.BasContext import _bas
from bas.BasBinanceTimeManager import basTimer, BasBinanceTimeInterval,\
    basTimeintervalWrapper
from bas.BasBinanceClientState import BasCandleTrackerTrackerState
from bas.BasBinanceCandleReader import basCandleReader
from bas.BasCoinManager import basCoinmanager



#see: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html

class BasThreadCandleTracker(QThread):
    
        
        
        def __init__(self, signal, params={}, parent=None):
            super(BasThreadCandleTracker, self).__init__(parent)
            self.state = BasCandleTrackerTrackerState.FirstRun
            
            #params:{symbol:limit,tiemInterval}
            self.params = params
            self.signal = signal
            self.symbol=None
            self.limit=None
            self.timeInterval=None
            
            if "symbol" in self.params:
                self.symbol = self.params["symbol"]
            if "limit" in self.params:
                self.limit = self.params["limit"]
            if "timeInterval" in self.params:
                self.timeInterval = self.params["timeInterval"]
            
            self.lastCandleInMongoDB=None
            
        
        
        def saveCandleDocs(self, timeInterval):
            if len(self.candleDocs)==0:
                return
            
            if len(self.candleDocs)==1:
                _bas.executer.mongoManager.saveUpdate(_bas.executer.mongoManager.candles,self.candleDocs[0])
                self.lastCandleInMongoDB = self.candleDocs[0]
            else:
                lastCandle = self.candleDocs.pop()
                for cd in self.candleDocs:
                    _bas.executer.mongoManager.saveUpdate(_bas.executer.mongoManager.candles,cd)
                #_bas.executer.mongoManager.candles.insert(candleDocs)
                #_bas.executer.mongoManager.candles.insert_one(lastCandle)
                _bas.executer.mongoManager.saveUpdate(_bas.executer.mongoManager.candles,lastCandle)
                self.lastCandleInMongoDB = lastCandle
            
        def saveCandles(self, candles, timeInterval):
            if len(candles)==0:
                return
            self.candleDocs = basCandleReader.mapMongoDoc(candles, timeInterval)
            self.saveCandleDocs(timeInterval)
            
            
         
        def doWork(self):
            self.signal.emit({"type":"candleTracker", "data":self.candles, "params":self.params})
            self.candles = _bas.executer.binanceManager.getCandles(
                symbol=self.symbol, 
                interval= basTimeintervalWrapper.kline(self.timeInterval), 
                limit=self.limit, 
                startTime=int(self.lastCandleInMongoDB["openTime"])
                )
            self.candleDocs = basCandleReader.mapMongoDoc(self.candles,self.timeInterval)

            if len(self.candleDocs)==1:# it returns the lastCandle with new info inside
                #_bas.executer.mongoManager.candles.update_one(candleDocs[0])
                _bas.executer.mongoManager.saveUpdate(_bas.executer.mongoManager.candles,self.candleDocs[0] )
                self.lastCandleInMongoDB = self.candleDocs[0]
            elif len(self.candleDocs)>1: # there are new candles and the old one inside.
                first = self.candleDocs[0]
                #_bas.executer.mongoManager.candles.update_one(candleDocs[0])
                _bas.executer.mongoManager.saveUpdate(_bas.executer.mongoManager.candles,self.candleDocs[0] )
                del self.candleDocs[0]
                self.saveCandleDocs(self.timeInterval)
                
            #self.saveCandles(self.candles, self.timeInterval)
            
        def run(self):
            self.waitTime = _bas.executer.configManager.config.bas.threads.candleTracker.waitTime
            if self.state.value==BasCandleTrackerTrackerState.FirstRun.value:
                if self.symbol==None or self.symbol not in basCoinmanager.coinSymbols:
                    self.symbol = _bas.executer.configManager.config.bas.default.trade.symbol
                if self.limit==None or self.limit <5 or self.limit>500:
                    self.limit= _bas.executer.configManager.config.bas.threads.candleTracker.limit
                if self.timeInterval==None or self.timeInterval< BasBinanceTimeInterval.OneMinute or self.timeInterval>BasBinanceTimeInterval.oneYear:
                    self.timeInterval= _bas.executer.configManager.config.bas.default.trade.timeInterval
        
                #fetchCount = _bas.executer.state.candleTracker.maxFetchCount
                self.candles = _bas.executer.binanceManager.getCandles(symbol=self.symbol, interval= basTimeintervalWrapper.kline(self.timeInterval), limit=self.limit)
                self.saveCandles(self.candles, self.timeInterval)
                self.state = BasCandleTrackerTrackerState.Running.value
            
            
            
            while True:
                self.doWork()
                time.sleep(self.waitTime)

