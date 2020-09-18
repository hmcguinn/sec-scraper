#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime 

from multiprocessing import Value
def init(): 
    global urlCount
    urlCount = Value('i', 0) 
    global time1 
    time1 = datetime.datetime.now() 
