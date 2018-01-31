'''
Created on Jan 12, 2018

@author: halil
'''
import time
import threading
from bas.BasContext import _bas
from bas.BasBinanceTimeManager import basTimer, BasBinanceTimeInterval,\
    basTimeintervalWrapper
from bas.BasBinanceClientState import BasThreadState
from bas.BasBinanceCandleReader import basCandleReader
from bas.BasCoinManager import basCoinmanager
import copy 
import json
from bson import json_util
from bas.BasExecuter import BasLocks_ClientThreads



#see: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html
#see: stop event https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch09s03.html


class BasThreadCandleReader(threading.Thread):
    
        
        def __init__(self, websocket=None, threadId="BasThreadCandleReader",params={}, name=None):
            self._stopevent = threading.Event( )
            threading.Thread.__init__(self)
            self.threadId = threadId
            self.name = name
            self.state = BasThreadState.FirstRun
            self.plotClient = params["plotClient"]
            self.websocket = websocket
            #params:{symbol:limit,tiemInterval}
            self.params = params
            self.symbol=None
            self.limit=None
            self.timeInterval=None
            #candles' ids are 'startTime'. while fetching, the candle having the most recent startTime should be recorded
            self.mostRecentCandle=None 
            self.candlePlots=[]
            
            if "symbol" in self.params:
                self.symbol = self.params["symbol"]
            if "limit" in self.params:
                self.limit = self.params["limit"]
            if "timeInterval" in self.params:
                self.timeInterval = self.params["timeInterval"]
            
            self.lastCandleInMongoDB=None

        
        def pushCandles(self, candles):
            #plotClientId, symbol, timeInterval, mostRecentCandle, 
            print("sending candles to plotClientId:"+self.plotClient.plotParams.plotId, candles)
            self.websocket.client.sendMessage(json_util.dumps({
            "plotClientId":self.plotClient.plotParams.plotId,
            "action":"retrieveCandles", 
            "symbol":self.plotClient.plotParams.symbol, 
            "timeInterval":self.plotClient.plotParams.timeInterval,
            "mostRecentCandle":self.mostRecentCandle, 
            "candles":candles}))
    
        
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
            
       
         
        def doWork(self):
            #self.signal.emit({"action":"candleTracker", "data":self.candles, "params":self.params})
            if self.mostRecentCandle==None:
                self.candleDocs = _bas.executer.mongoManager.getCandles(
                symbol=self.symbol, 
                timeInterval= self.timeInterval, 
                limit=self.limit 
                )
                

            else:
                self.candleDocs = _bas.executer.mongoManager.getCandles(
                symbol=self.symbol, 
                timeInterval= self.timeInterval,
                openTime=self.mostRecentCandle["openTime"],
                limit=self.limit 
                )
                
            if len(self.candleDocs)>0:
                a = self.candleDocs[-1]
                self.mostRecentCandle = basCandleReader.copyDoc(a)
                self.pushCandles(self.candleDocs)

            
        def run(self):
            print ("candle reader started!")
            self.waitTime = _bas.executer.configManager.config.bas.threads.candleWriter.waitTime
            if self.state.value==BasThreadState.FirstRun.value:
                if self.symbol==None or self.symbol not in basCoinmanager.coinSymbols:
                    self.symbol = _bas.executer.configManager.config.bas.default.trade.symbol
                if self.limit==None or self.limit<5 or self.limit>500:
                    self.limit= _bas.executer.configManager.config.bas.threads.candleWriter.limit
                if self.timeInterval==None or self.timeInterval< BasBinanceTimeInterval.OneMinute or self.timeInterval>BasBinanceTimeInterval.oneYear:
                    self.timeInterval= _bas.executer.configManager.config.bas.default.trade.timeInterval
        
                #fetchCount = _bas.executer.state.candleTracker.maxFetchCount
                #self.candleDocs = _bas.executer.mongoManager.getCandles(symbol=self.symbol, timeInterval= self.timeInterval, limit=self.limit)
                
                self.state = BasThreadState.Running.value
#                 if len(self.candleDocs)>0:
#                     a = self.candleDocs[-1]
#                     self.mostRecentCandle = basCandleReader.copyDoc(a)
#                     self.pushCandles(self.candleDocs)

                
            
            while not self._stopevent.isSet( ):
                #time.sleep(self.waitTime)
                self._stopevent.wait(self.waitTime)
                self.doWork()
                self.stopIfClientLost()
                
        
        def stopIfClientLost(self):
            clientId_ = self.params.plotClient.clientInfo.clientId
            if clientId_ not in BasLocks_ClientThreads:
                self.stopWorking()
            
       
        
        
        def stopWorking(self, timeout=15.0):
            """ Stop the thread and wait for it to end. """
            self.websocket.close()
            self._stopevent.set( )
            threading.Thread.join(self, timeout)
                

