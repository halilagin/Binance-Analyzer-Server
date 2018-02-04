'''
Created on Jan 12, 2018

@author: halil
'''
import time
from bas.BasContext import _bas
from bas.BasBinanceTimeManager import basTimer
from bas.BasBinanceCandleReader import basCandleReader
import pymongo
from pymongo import *
import threading
from bas.BasWebSocket import BasWebSocket, BasWebSocketCandle_clients
from bas.BasWebSocketWriterManager import BasWebSocketWriterManager
from bas.BasVars import BasLocks_initializer
    

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
            BasLocks_initializer.acquire() 
            time.sleep(1)


            
            while len(BasWebSocketCandle_clients)==0:
                print("waiting a client to connect...")
                time.sleep(2)
            
            BasWebSocketWriterManager().pushServerInitializerStarted()
            
            #self.signal.emit({"source": "initializerThread", "data":{"action":"showProgressBar","progress":0.1}} )
            time.sleep(1)
            self.initMongoDB()
            for i in range(5):
                time.sleep(3)
                BasLocks_initializerProgress=0.1*(i+1)
                BasWebSocketWriterManager().pushServerInitializingInProgress(BasLocks_initializerProgress)
                print("init.progress:",BasLocks_initializerProgress)
                #self.signal.emit({"source": "initializerThread", "data":{"progress":0.1, "action":None}} )
            
            _bas.executer.configManager.config.bas.application.firstRun=0
            _bas.executer.configManager.write()
            
            _bas.executer.startThreads()
            BasWebSocketWriterManager().pushServerInitializerFinished()
            BasLocks_initializer.release()

            #self.signal.emit({"source": "initializerThread", "data":{"action":"closeProgressBar","progress":1}} )
            