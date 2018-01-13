'''
Created on Jan 12, 2018

@author: halil
'''

from enum import Enum
from bas.BasHashObjectSerializer import BasHashObjectSerializer




class BasCandleTrackerTrackerState(Enum):
    pass
    IDLE=0
    STOP=10
    FirstRun=20
    Running=30
    ABORT=40
    UNKNOWN=50
    

class BasClientState(object):
    
    def __init__(self):
        pass
        self.state_ = {
            "candleTracker":{
                "maxFetchCount":500,
                "currentFetchCount":10,
                "state":BasCandleTrackerTrackerState.FirstRun.value
                }
            }
        self.state = BasHashObjectSerializer(self.state_)




