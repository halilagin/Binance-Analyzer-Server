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
from bas.BasExecuter import BasLocks_ClientThreads


# see sudo pip3.6 install git+https://github.com/dpallot/simple-websocket-server.git
#see https://github.com/dpallot/simple-websocket-server

#from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class BasWebSocketClient(object):
    pass
    def __init__(self, clientIndex=None, id=None, client=None):
        self.clientIndex = clientIndex
        self.id = uuid.uuid4().__str__()
        self.client = client
        
    


BasWebSocketCandle_clients = {}

class BasWebSocket(WebSocket):

    def handleMessage(self):
    
        #if client != self:
        #client.sendMessage(self.address[0] + u' - ' + self.data)
        clientMessage = BasHashObjectSerializer( json_util.loads(self.data) )
        message = None
        if clientMessage.action=="fetchServerState":
            message = {"serverState":_bas.executer.configManager.config.bas.application.firstRun}
            self.sendMessage(message)
        elif clientMessage.action=="finishNewSubscription":
            #dont do anything it is already subscribed!
            self.finishNewSubscription(clientMessage)
        elif clientMessage.action=="finishReSubscription":
            #there is a client registered in server side with the id clientIdInServerSide.
            #that client received new subscription. replace clientIdInLocalstorage with clientIdInServerSide
            self.finishReSubscription(clientMessage)
        
        elif clientMessage.action=="registerCandlePlot":
            print("registerCandlePlot:",self.data)
            
            if clientMessage.clientInfo.clientId not in BasLocks_ClientThreads:
                BasLocks_ClientThreads[clientMessage.clientInfo.clientId] ={}
                
            if "threads" not in BasLocks_ClientThreads[clientMessage.clientInfo.clientId]:
                BasLocks_ClientThreads[clientMessage.clientInfo.clientId]["threads"]=[]
            
            candleReader = BasThreadCandleReader(websocket=self, threadId="candleReader_"+clientMessage.plotParams.plotId, params={"plotClient":clientMessage})
            BasLocks_ClientThreads[clientMessage.clientInfo.clientId]["threads"].append(candleReader) 
            candleReader.start()
                
        
            
        print ("websocketserver.handlemessage:",self.data)
    
   
#see:stop thread  https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch09s03.html
    def finishReSubscription (self, message):
        pass
        #stop threads
        if message.clientInfo.clientId not in BasLocks_ClientThreads:
            return
        if "threads" not in BasLocks_ClientThreads[message.clientInfo.clientId]:
            return
        
        if  len(BasLocks_ClientThreads[message.clientInfo.clientId]["threads"])==0:
            return
        
        for thread_ in BasLocks_ClientThreads[message.clientInfo.clientId]["threads"]:
            thread_.stopWorking()
            
        
        
        #remove previously subscribed websocket and stop threads related.
        clientId = message.clientInfo.clientIdPreviouslySubscribed
        for ws in BasWebSocketCandle_clients:
            if ws.id==clientId:
                BasWebSocketCandle_clients.remove(ws.id)
         
        self.ackSubscription({
            "action": "ackSubscription",
            "clientId":message.clientInfo.clientIdNewlyBeingSubscribed
            } )
        
    
    def finishNewSubscription(self, message):
         
        self.ackSubscription({
            "action": "ackSubscription",
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
                clientIndex=len(BasWebSocketCandle_clients),
                client=self)
        BasWebSocketCandle_clients[client_.id]=client_
        
        clientMessage = json_util.dumps( {
            "action": "startSubscription",
            "clientIndex":client_.clientIndex,
            "websocketServerId":client_.id,
            
            "id": "nativeClient"
            } )

        self.sendMessage(clientMessage)
#         for client in BasWebScoketCandle_clients:
#             client.sendMessage(self.address[0] + u' - connected')
#             BasWebScoketCandle_clients.append(self)

    def handleClose(self):
        BasWebSocketCandle_clients.remove(self)
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
    
        
        