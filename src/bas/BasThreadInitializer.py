'''
Created on Jan 12, 2018

@author: halil
'''
import time
from bas.BasContext import _bas
from bas.BasBinanceTimeManager import basTimer
from bas.BasBinanceClientState import BasCandleTrackerTrackerState
from bas.BasBinanceCandleReader import basCandleReader
import pymongo
from pymongo import *
import threading
from bas.BasWebSocket import BasWebSocket, BasWebSocketCandle_clients,\
    WebSocketWriterManager

#see: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html

class BasThreadInitializer(threading.Thread):
        
        def __init__(self, threadID="BasThreadInitializer", name=None):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            
            
            
        def initMongoDB(self):
            pass
            _bas.executer.mongoManager.candles.create_index(
            [
             ("timeInterval", pymongo.ASCENDING),
             ("openTime", pymongo.ASCENDING)
            ], unique=True)
            
        def run(self):
            pass    
            _bas.executer.locks["initializerLock"].acquire()
            time.sleep(1)

            _bas.executer.locks["initializerProgress"]=0.0
            print("init.progress:",_bas.executer.locks["initializerProgress"])


            
            while len(BasWebSocketCandle_clients)==0:
                print("waiting a client for connecting...")
                time.sleep(2)
            
            WebSocketWriterManager().pushServerInitializerStarted()
            
            #self.signal.emit({"source": "initializerThread", "data":{"action":"showProgressBar","progress":0.1}} )
            time.sleep(1)
            self.initMongoDB()
            for i in range(5):
                time.sleep(3)
                _bas.executer.locks["initializerProgress"]=0.1*(i+1)
                WebSocketWriterManager.pushServerInitializingInProgress(_bas.executer.locks["initializerProgress"])
                print("init.progress:",_bas.executer.locks["initializerProgress"])
                #self.signal.emit({"source": "initializerThread", "data":{"progress":0.1, "action":None}} )
            
            _bas.executer.configManager.config.bas.application.firstRun=1
            _bas.executer.configManager.write()
            WebSocketWriterManager().pushServerInitializerFinished()

            #self.signal.emit({"source": "initializerThread", "data":{"action":"closeProgressBar","progress":1}} )
            