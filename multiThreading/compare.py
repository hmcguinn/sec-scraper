#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os 
import pandas as pd 
import numpy as np
import glob

cikList = [] 
TickerFile = pd.read_csv("cik.csv") 
Tickers = TickerFile['CIK'].tolist()

newSet = {} 
h = 0
j = 0
"""
for f in glob.glob("./data/*_data.xlsx"):
    s = str(f)
    s = s.strip("./data/")
    s = s.rstrip("_data.xlsx")
    newSet[s] = None
    #print(s) 
"""

Validated = pd.read_excel("validate_last.xlsx")
validatedSet = Validated['CIK'].tolist() 

for i in validatedSet: 
    newSet[str(i)] = None 

print(newSet)

emptySet = []
for i in range(len(Tickers)): 
    #print(Tickers[i])
    if (str(Tickers[i]) in newSet): 
        #print('-----------------------------------------------')         
        j += 1
        pass
    else: 
        h += 1 
        n = Tickers[i]
        emptySet.append(n)
        print("Not in: " + str(Tickers[i]))
        pass

s = Tickers[0]
print(h)
print(j)
df = pd.DataFrame(emptySet, columns =["CIK"]) 
df.to_csv("notIn.csv")



