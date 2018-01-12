'''
Created on Jan 12, 2018

@author: halil
'''
from PyQt5.Qt import QThread
import time
from bas.BasContext import _bas
from bas.BasBinanceTimeManager import basTimer
from bas.BasBinanceClientState import BasCandleTrackerTrackerState
from bas.BasBinanceCandleReader import basCandleReader



#see: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html

class BasThreadCandleTracker(QThread):
        
        def __init__(self, signal, parent=None):
            self.signal = signal
            super(BasThreadCandleTracker, self).__init__(parent)
            self.waitTime = _bas.executer.configManager.config.bas.thread.candleTracker.waitTime
            
            
        def saveCandles(self, candles, timeInterval):
            _bas.executer.mongoManager.candles.insert(candles)
            basCandleReader.mapMongoDoc(candles, timeInterval)

            _bas.executer.mongoManager.candles.insert(candles)
        
        def run(self):
            
                
            while True:
                if _bas.executer.state.candleTracker.state.value==BasCandleTrackerTrackerState.FirstRun.value:
                    #fetchCount = _bas.executer.state.candleTracker.maxFetchCount
                    symbol = _bas.executer.configManager.config.bas.default.trade.symbol
                    limit = _bas.executer.configManager.config.bas.candleTracker.limit
                    timeInterval = _bas.executer.configManager.config.bas.default.trade.timeInterval
                    candles = _bas.executer.binanceManager.getCandles(symbol=symbol, interval=timeInterval, limit=limit)
                    self.saveCandles(candles, timeInterval)
                time.sleep(self.waitTime)
                self.signal.emit({"type":"test", "data":"hello world!!!"})
                print (time.time())
