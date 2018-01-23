'''
Created on Jan 21, 2018

@author: halil
'''
from SimpleWebSocketServer.SimpleWebSocketServer import SimpleWebSocketServer
from SimpleWebSocketServer.SimpleWebSocketServer import WebSocket
from bas.BasContext import _bas
import json
import copy
from bas.BasHashObjectSerializer import BasHashObjectSerializer
# see sudo pip3.6 install git+https://github.com/dpallot/simple-websocket-server.git
#see https://github.com/dpallot/simple-websocket-server

#from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

class BasWebSocketClient(object):
    pass
    def __init__(self, clientIndex=None, id=None, client=None):
        self.clientIndex = clientIndex
        self.id = id
        self.client = client
        
    


BasWebSocketCandle_clients = []
class BasWebSocket(WebSocket):

    def handleMessage(self):
        for client in BasWebSocketCandle_clients:
            #if client != self:
            client.sendMessage(self.address[0] + u' - ' + self.data)
            clientMessage = BasHashObjectSerializer( json.loads(self.data) )
            message = None

            if clientMessage.action=="fetchServerState":
                message = {"serverState":_bas.executer.configManager.config.bas.application.firstRun}
                client.sendMessage(message)
            
        print ("websocketserver.handlemessage:",self.data)
    
   
    
    
    
    def handleConnected(self):
        print(self.address, 'connected')
        
        client_ =  BasWebSocketClient(
                id="nativeClient",
                clientIndex=len(BasWebSocketCandle_clients),
                client=self)
        BasWebSocketCandle_clients.append(client_)
        
        clientMessage = json.dumps( {
            "action": "subscribe",
            "clientIndex":client_.clientIndex,
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


class WebSocketWriterManager(object):
    pass

    @staticmethod
    def pushMessage(message):
        for c in BasWebSocketCandle_clients:
            c.client.sendMessage(json.dumps(message))
    
    
    
    
    @staticmethod
    def pushServerInitializerStarted():
        WebSocketWriterManager.pushMessage({"action":"ServerInitializerStarted", "progress":0.0})
    
    @staticmethod
    def pushServerInitializingInProgress(progress):
        WebSocketWriterManager.pushMessage({"action":"ServerInitializingInProgress", "progress":progress})
    
    @staticmethod
    def pushServerInitializerFinished():
        WebSocketWriterManager.pushMessage({"action":"ServerInitializerFinished", "data":None})
    
        

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
    
        
        