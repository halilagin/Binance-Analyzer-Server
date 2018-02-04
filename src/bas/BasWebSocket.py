'''
Created on Jan 21, 2018

@author: halil
'''
from SimpleWebSocketServer.SimpleWebSocketServer import SimpleWebSocketServer
from SimpleWebSocketServer.SimpleWebSocketServer import WebSocket
from bas.BasContext import _bas
from bas.BasHashObjectSerializer import BasHashObjectSerializer
from bson import json_util
from bas.BasThreadCandleReader import BasThreadCandleReader
import uuid
from bas.BasVars import BasWebSocketCandle_clients, BasLocks_ClientThreads,\
    BasLocks_PingedWebSocketClients
import timeit


# see sudo pip3.6 install git+https://github.com/dpallot/simple-websocket-server.git
#see https://github.com/dpallot/simple-websocket-server

#from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class BasWebSocketClient(object):
    pass
    def __init__(self,  id=None, client=None):
        self.id = uuid.uuid4().__str__()
        self.client = client
        
    



class BasWebSocket(WebSocket):

    def handleMessage(self):
    
        #if client != self:
        #client.sendMessage(self.address[0] + u' - ' + self.data)
        clientMessage = BasHashObjectSerializer( json_util.loads(self.data) )
        message = None
        if clientMessage.action=="fetchServerState":
            message = {"serverState":_bas.executer.configManager.config.bas.application.firstRun}
            self.sendMessage(message)
        elif clientMessage.action=="startNewSubscription":
            #dont do anything it is already subscribed!
            print("finishNewSubscription",clientMessage)
            self.finishNewSubscription(clientMessage)
            
        elif clientMessage.action=="startReSubscription":
            #there is a client registered in server side with the id clientIdInServerSide.
            #that client received new subscription. replace clientIdInLocalstorage with clientIdInServerSide
            print("startReSubscription",clientMessage)
            self.startReSubscription(clientMessage)
        
        elif clientMessage.action=="registerCandlePlot":
            print("registerCandlePlot:",self.data)
            self.registerCandlePlot(clientMessage)
        elif clientMessage.action=="ping":
            self.ping(clientMessage)
            
            
                
        
            
        print ("websocketserver.handlemessage:",self.data)
    
    
    def ping(self, message):
        if 'clientId' in message.__dict__:
            if message.clientId not in BasLocks_PingedWebSocketClients:
                BasLocks_PingedWebSocketClients[message.clientId]={}
                BasLocks_PingedWebSocketClients[message.clientId]["accessTime"]=timeit.time.time()
                BasLocks_PingedWebSocketClients[message.clientId]["plots"]={}
        if 'plotId' in message.__dict__:
            if "plots" not in BasLocks_PingedWebSocketClients[message.clientId]:
                BasLocks_PingedWebSocketClients[message.clientId]["plots"]={}
            BasLocks_PingedWebSocketClients[message.clientId]["plots"][message.plotId]=timeit.time.time()
        
                
    
    def registerCandlePlot(self,clientMessage):
        if clientMessage.clientInfo.clientId not in BasLocks_ClientThreads:
            BasLocks_ClientThreads[clientMessage.clientInfo.clientId] ={}
                
        if "threads" not in BasLocks_ClientThreads[clientMessage.clientInfo.clientId]:
            BasLocks_ClientThreads[clientMessage.clientInfo.clientId]["threads"]={}
        
        if "candleReader_"+clientMessage.plotParams.plotId not in  BasLocks_ClientThreads[clientMessage.clientInfo.clientId]["threads"]:
            threadId = "candleReader_"+clientMessage.plotParams.plotId  #plotClientId
            clientId=clientMessage.clientInfo.clientId
            candleReader = BasThreadCandleReader(websocket=self, threadId=threadId, params={"plotClient":clientMessage})
            BasLocks_ClientThreads[clientId]["threads"][threadId]=candleReader 
            candleReader.start()
   
#see:stop thread  https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch09s03.html
    def startReSubscription (self, message):
        pass
        #stop threads
        
        if message.clientInfo.clientIdPreviouslySubscribed not in BasLocks_ClientThreads:
            self.ackSubscription({
                "action": "ackReSubscription",
                "clientId":message.clientInfo.clientIdNewlyBeingSubscribed
                })
            return
        if "threads" not in BasLocks_ClientThreads[message.clientInfo.clientIdPreviouslySubscribed]:
            self.ackSubscription({
                "action": "ackReSubscription",
                "clientId":message.clientInfo.clientIdNewlyBeingSubscribed
                })
            return
        
        if  len(BasLocks_ClientThreads[message.clientInfo.clientIdPreviouslySubscribed]["threads"])==0:
            self.ackSubscription({
                "action": "ackReSubscription",
                "clientId":message.clientInfo.clientIdNewlyBeingSubscribed
                })
            return
        
        for thread_ in BasLocks_ClientThreads[message.clientInfo.clientIdPreviouslySubscribed]["threads"]:
            thread_.stopWorking()
            
        
        
        #remove previously subscribed websocket and stop threads related.
        clientId = message.clientInfo.clientIdPreviouslySubscribed
        for ws in BasWebSocketCandle_clients:
            if ws.id==clientId:
                del BasWebSocketCandle_clients[ws.id]
                
         
        self.ackSubscription({
            "action": "ackReSubscription",
            "clientId":message.clientInfo.clientIdNewlyBeingSubscribed
            } )
        
    
    def finishNewSubscription(self, message):
         
        self.ackSubscription({
            "action": "ackNewSubscription",
            "clientId":message.clientInfo.clientId
        } )
        
    
    def ackSubscription(self, message):
        pass
        clientMessage = json_util.dumps(message )
        self.sendMessage(clientMessage)
        
        
    def handleConnected(self):
        print(self.address, 'connected')
        
        client_ =  BasWebSocketClient(
                id=uuid.uuid4(),#random uuid
                client=self)
        BasWebSocketCandle_clients[client_.id]=client_
        
        clientMessage = json_util.dumps( {
            "action": "startSubscription",
            "clientId":client_.id,
            "websocketServerId":client_.id,
            
            "id": "nativeClient"
            } )

        self.sendMessage(clientMessage)
#         for client in BasWebScoketCandle_clients:
#             client.sendMessage(self.address[0] + u' - connected')
#             BasWebScoketCandle_clients.append(self)

    def handleClose(self):
        #del BasWebSocketCandle_clients[ws.id]
        #BasWebSocketCandle_clients.remove(self)
        print(self.address, 'closed')
#         for client in BasWebScoketCandle_clients:
#             client.sendMessage(self.address[0] + u' - disconnected')


class BasWebSocketServer():
    '''
    classdocs
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        #super(BasThreadWebSocketCandle, self).__init__(parent)
            
        
    def run(self):
        host = _bas.executer.configManager.config.bas.websockets.candle.host
        port = _bas.executer.configManager.config.bas.websockets.candle.port
        self.host = host+":"+str(port)
        self.server = SimpleWebSocketServer(host, port, BasWebSocket)
        self.server.serveforever()
    
        
        