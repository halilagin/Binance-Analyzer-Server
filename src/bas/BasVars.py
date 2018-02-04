import threading

BasLocks_WebSocketCandleReaderClients=[]
BasLocks_WebSocketCandleReaderClients_lock=threading.Lock()
BasLocks_initializer=threading.Lock()
BasLocks_initializerProgress=0.0

#hash <client id,[threads]> 
BasLocks_ClientThreads={}

#BasWebSocketCandle_clients = {"clientId":{"lastAccessTime":-1, "plots":{}}}
#BasWebSocketCandle_clients = {"bc":{"accessTime":34583475, "plots":{"afwerwe":983456387465}}}
BasWebSocketCandle_clients = {}
BasLocks_PingedWebSocketClients={}
