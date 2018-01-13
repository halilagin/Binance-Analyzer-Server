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
import pymongo
from pymongo import *


#see: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html

class BasThreadInitializer(QThread):
        
        def __init__(self, signal, parent=None):
            self.signal = signal
            super(BasThreadInitializer, self).__init__(parent)
            
            
        def initMongoDB(self):
            pass
            _bas.executer.mongoManager.candles.create_index(
            [
             ("timeInterval", pymongo.ASCENDING),
             ("openTime", pymongo.ASCENDING)
            ], unique=True)
            
        def run(self):
            pass    
            time.sleep(1)

            self.signal.emit({"source": "initializerThread", "data":{"action":"showProgressBar","progress":0.1}} )
            time.sleep(1)
            self.initMongoDB()
            for i in range(10):
                time.sleep(1)
                self.signal.emit({"source": "initializerThread", "data":{"progress":0.1, "action":None}} )
            
            _bas.executer.configManager.config.bas.application.firstRun=0
            _bas.executer.configManager.write()
            self.signal.emit({"source": "initializerThread", "data":{"action":"closeProgressBar","progress":1}} )
