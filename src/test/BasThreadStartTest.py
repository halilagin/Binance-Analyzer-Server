'''
Created on Jan 24, 2018

@author: halil
'''
from bas.BasThreadCandleReader import BasThreadCandleReader

if __name__ == '__main__':
    candleReader = BasThreadCandleReader(threadId="candleReader_", params={"plotClient":""})
    candleReader.start()
