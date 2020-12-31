#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import settings
import pandas as pd
import re
import requests
import time
import urllib.request as url
from bs4 import BeautifulSoup
import lxml
import os
import datetime
import multiprocessing  
from multiprocessing import Pool, Value, Manager
from opensPerSecond import opensPerSecond
from getList import get_list_multi
from runScraper import runScraper
import traceback

# Import CIK's to scrape  
cikList = [] 
TickerFile = pd.read_csv("cik.csv")
#TickerFile = pd.read_csv("cik.csv")
Tickers = TickerFile['CIK'].tolist()
print(Tickers)

# Counter for URL opens 
#urlCount = Value('i', 0)
settings.init() 

searchURLs = [] 

# Subset of the CIK's to scrape on this run 
#tickerArray = Tickers[10000:]
tickerArray = Tickers
#tickerArray = [1600132]


# Actually get URLs to scrape 
with Pool(400) as p:
    searchURLs.extend(p.map(get_list_multi, tickerArray))
#for i in range(len(tickerArray)): 
#    searchURLs.extend(get_list_multi(tickerArray[i]))
p.close()
p.join()

# Record time 
time2 = datetime.datetime.now() 
elapsedTime = time2 - settings.time1
elapsedTime
print(divmod(elapsedTime.total_seconds(), 60))
print(str(settings.urlCount.value) + " URL opens")
print("Opens per second = " + str((settings.urlCount.value/elapsedTime.total_seconds())))

# Store first set of URLs 
toScrape = pd.DataFrame(searchURLs)
toScrape.to_pickle("./firstFunction.pkl")
toScrape.to_excel("toScrape.xlsx")


# Actually scrape URLs  
with Pool(400) as p1:
    (p1.map(runScraper, searchURLs))
#for i in range(len(searchURLs)): 
#    runScraper(searchURLs)

p1.close()
p1.join()

# Record time 
print(divmod(elapsedTime.total_seconds(), 60))
print(str(settings.urlCount.value) + " URL opens")
print("Opens per second = " + str((settings.urlCount.value/elapsedTime.total_seconds())))


