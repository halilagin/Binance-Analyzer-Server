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
            #client.sendMessage(self.address[0] + u' - ' + self.data)
            clientMessage = BasHashObjectSerializer( json_util.loads(self.data) )
            message = None
            if clientMessage.action=="fetchServerState":
                message = {"serverState":_bas.executer.configManager.config.bas.application.firstRun}
                client.sendMessage(message)
            elif clientMessage.action=="registerCandlePlot":
                print("registerCandlePlot:",self.data)
                
                candleReader = BasThreadCandleReader(websocket=client, threadId="candleReader_"+clientMessage.plotParams.plotId, params={"plotClient":clientMessage})
#                 #_bas.executer.threads["candleReaders"].append(candleReader)
                candleReader.start()
                
        
            
        print ("websocketserver.handlemessage:",self.data)
    
   
    
    
    
    def handleConnected(self):
        print(self.address, 'connected')
        
        client_ =  BasWebSocketClient(
                id="nativeClient",
                clientIndex=len(BasWebSocketCandle_clients),
                client=self)
        BasWebSocketCandle_clients.append(client_)
        
        clientMessage = json_util.dumps( {
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
    
        
        