#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime 
import settings 
import time 
def opensPerSecond(opens, time3): 
    timeNow = datetime.datetime.now() 
    elapsedTime = timeNow - time3

    opens = settings.urlCount.value/elapsedTime.total_seconds()
    if(opens > 9.5): 
        pass
        #print("Going too fast, sleeping " + str(opens))
        #time.sleep(0.2)
        #print(opens)
    return opens 

