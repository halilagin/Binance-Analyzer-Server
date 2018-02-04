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
from bas.BasVars import BasLocks_ClientThreads, BasLocks_PingedWebSocketClients,\
    BasWebSocketCandle_clients
import timeit



#see: http://pyqt.sourceforge.net/Docs/PyQt5/signals_slots.html
#see: stop event https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch09s03.html


class BasThreadCleaner(threading.Thread):
    
        
        def __init__(self, websocket=None, threadId="BasThreadCleaner",params={}, name=None):
            self._stopevent = threading.Event( )
            threading.Thread.__init__(self)
            self.threadId = threadId
            self.name = name

        
         
        def doWork(self):
            pass
        
            for clientId in BasLocks_PingedWebSocketClients:
                c_ = BasLocks_PingedWebSocketClients[clientId]
                
                if (timeit.time.time()-c_["accessTime"])>self.killWebSocketTimeInterval:
                    self.cleanClientThreads(clientId,c_)
                else:
                    self.cleanClientPlotThreads(clientId, c_)
        def run(self):
            print ("[ThreadCleaner] started!")
            self.waitTime = _bas.executer.configManager.config.bas.threads.cleaner.waitTime
            self.killPlotTimeInterval = _bas.executer.configManager.config.bas.threads.cleaner.plot.killTimeInterval
            self.killWebSocketTimeInterval = _bas.executer.configManager.config.bas.threads.cleaner.websocket.killTimeInterval

            while not self._stopevent.isSet( ):
                time.sleep(self.waitTime)
                self._stopevent.wait(self.waitTime)
                self.doWork()
                
        
       
        
        
        
        def stopWorking(self, timeout=15.0):
            """ Stop the thread and wait for it to end. """
            self._stopevent.set( )
            threading.Thread.join(self, timeout)
                


        def cleanClientPlotThreads(self,clientId, client_):
            print ("[ThreadCleaner] cleaning the plots of client id", clientId)
            
            if "plots" not in client_:
                return
            
            for plotId in client_["plots"]:
                threadId = "candleReader_"+plotId  #plotClientId
                lastPlotAccessTime = client_["plots"][plotId]
                if (timeit.time.time()-lastPlotAccessTime)>self.killPlotTimeInterval:
                    BasLocks_ClientThreads[clientId]["threads"][threadId].stopWorking() 
            

        def cleanClientThreads(self, clientId, client_):
            print ("[ThreadCleaner] cleaning the client id", clientId)

            if clientId  not in BasLocks_ClientThreads:
                return
        
            if "threads" not in BasLocks_ClientThreads[clientId]:
                return
            
            self.cleanClientPlotThreads(clientId, client_)
            
            for ws in BasWebSocketCandle_clients:
                pass
                if ws.id==clientId:
                    lastWSAccessTime = BasLocks_ClientThreads[clientId]["accessTime"]
                    if (timeit.time.time()-lastWSAccessTime)>self.killWebSocketTimeInterval:
                        BasWebSocketCandle_clients[clientId].close()
                
                
            