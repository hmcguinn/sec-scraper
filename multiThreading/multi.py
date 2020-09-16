#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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
import traceback

cikList = [] 
TickerFile = pd.read_csv("cik.csv")
Tickers = TickerFile['CIK'].tolist()
#print(Tickers)

urlCount = Value('i', 0)

def opensPerSecond(opens, time3): 
    timeNow = datetime.datetime.now() 
    elapsedTime = timeNow - time3

    opens = urlCount.value/elapsedTime.total_seconds()
    if(opens > 9.5): 
        #print("Going too fast, sleeping " + str(opens))
        time.sleep(0.2)
    #print(opens)
    return opens 


def get_list_multi(cik1):
    global urlCount
    href = []
    #global urlCount 
    #urlCount = 0
    try:
        cik = cik1
        print("cik is " + str(cik))
        base_url_part1 = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
        base_url_part2 = "&type=&dateb=&owner=&start="
        base_url_part3 = "&count=100&output=xml"

        for page_number in range(0,100000,100):
            base_url = base_url_part1 + str(cik) + base_url_part2 + str(page_number) + base_url_part3
            #print(page_number) 
            #print(base_url)
            with urlCount.get_lock():
                urlCount.value += 1 
                #print(urlCount.value)
                opensPerSecond(urlCount.value,time1)

            sec_page = url.urlopen(base_url)
            sec_soup = BeautifulSoup(sec_page, "lxml")
            #print(sec_soup.prettify())
            filings = sec_soup.findAll('filing')
            if(len(filings)==0): 
                break

            for filing in filings:
                #print(filing)
                #time.sleep(.05)
                report_year = int(filing.datefiled.get_text()[0:4])
                if (filing.type.get_text() == "4") & (report_year >= 2005):
                    #print(filing.filinghref.get_text())
                    href.append(filing.filinghref.get_text())
                elif(filing.type.get_text() == "3") & (report_year >= 2005):
                    #print("form 3 ++++++++++++++++++++++ " + filing.filinghref.get_text())
                    href.append(filing.filinghref.get_text())
                elif(filing.type.get_text() == "4/A") & (report_year >= 2005):
                    #print("form 3 ++++++++++++++++++++++ " + filing.filinghref.get_text())
                    href.append(filing.filinghref.get_text())
                elif(filing.type.get_text() == "3/A") & (report_year >= 2005):
                    #print("form 3 ++++++++++++++++++++++ " + filing.filinghref.get_text())
                    href.append(filing.filinghref.get_text())
    except Exception as inst: 
        print("some exception occured")
        print(inst)
        pass

    return (href)

def runScraper(array): 
    global urlCount
    global m 
    
    pokemon = []
    numArray = 0
    cik = ""
    for x in array:
        
        try:
            numArray += 1
            individualName = None
            issuerName = None
            issuerCik = None
            date = None
            isDirector = None
            isOfficer = None
            isTenPercentOwner = None
            isOther = None
            reporterTitle = None
            documentType = None
            reporterCik = None

            
           
            #print("x is " + x)
            exampleURL = x

            req = requests.get(exampleURL, headers)
            soup1 = BeautifulSoup(req.content, 'xml')
            with urlCount.get_lock():
                urlCount.value += 1 
                #print(urlCount.value)
                opensPerSecond(urlCount.value,time1)

            #print(exampleURL)
            s = None
            #print(soup1.prettify())
            for link in soup1.find_all('a'):
                if("xml" in link.text):
                    newLink = link.text
                    #print(newLink)
                    break
            #print(link.text)

            x = exampleURL.split("/")

            for i in range(0,len(x)-1):
                if(s):
                    s = s + "/" + x[i]
                #print(s)
                else:
                    s = x[i]
            s =   s + "/" + newLink
            s.lstrip("/")
            #print(("final s is " + s)
            req2 = requests.get(s, headers)
            soup = BeautifulSoup(req2.content, 'lxml')
            with urlCount.get_lock():
                urlCount.value += 1 
                #print(urlCount.value)
                opensPerSecond(urlCount.value,time1)

            #print(exampleURL)
            
            if soup.rptownercik:  
                reporterCik = soup.rptownercik.string
                reporterCik = reporterCik.lstrip("0")
            if soup.rptownername:  
                individualName = soup.rptownername.string
                individualName = individualName.title()
            if soup.issuername: 
                issuerName = soup.issuername.string
            if soup.issuercik: 
                issuerCik = soup.issuercik.string
                issuerCik = issuerCik.lstrip("0")
            if(cik == ""): 
                cik = issuerCik
            if soup.periodofreport:  
                date = soup.periodofreport.string 
            length = len(array)
            #print(length)
            #print(numArray)
            #print(issuerCik)
            print(str(numArray) + " " + "of " + str(length) + "\t\t\t\t" + "CIK: " + issuerCik + 
                                    "\t\t\t ToDo: \t\t\t" + 
                                     str(round(((numArray/length)*100),2)) + "%") 
            if soup.isdirector: 
                isDirector = soup.isdirector.string
            if(isDirector == '1'):
                isDirector = "Yes"
            else:
                isDirector = "No"
            if soup.isofficer: 
                isOfficer = soup.isofficer.string
            if(isOfficer == '1'):
                isOfficer = "Yes"
            else:
                isOfficer = "No"

            if soup.istenpercentowner:
                isTenPercentOwner = soup.istenpercentowner.string
            if(isTenPercentOwner == '1'):
                isTenPercentOwner = "Yes"
            else:
                isTenPercentOwner = "No"

            if soup.isother: 
                isOther = soup.isother.string
            if(isOther == '1'):
                isOther = "Yes"
            else:
                isOther = "No"

            if soup.officertitle:
                reporterTitle = soup.officertitle.string
            if soup.documenttype:
                documentType = soup.documenttype.string
        
            
            form4Object = {"issuerName": issuerName, "issuerCik": issuerCik, "individualName": individualName,
            "reporterCik": reporterCik, "Director?": isDirector,
            "Officer?": isOfficer, "Ten Percent?": isTenPercentOwner,
            "Other?": isOther, "Title": reporterTitle, "Date": date,
            "Form": documentType, "URL": s}
            #pokemon = [issuerName, issuerCik, individualName, reporterCik, isDirector, isOfficer, isTenPercentOwner, isOther, reporterTitle
            #           , isOther, reporterTitle, data, documentType, s]
         
             
            pokemon.append(form4Object)
            #print(pokemon)
            #rows.append(pokemon)
        except Exception as inst: 
            print("threw an error " + str(s) + " " + str(exampleURL)) 
            print(traceback.format_exc())
            pass
    print(pokemon)
    returnDf = pd.DataFrame(pokemon)
    dataString = "./data/" + str(cik) + "_data.xlsx"
    returnDf.to_excel(dataString)
    #print("RETURNINGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    #print(n)
    #return returnDf
    #print(m)
    return 


n = [] 
tickerArray = Tickers[0:1000]
#tickerArray = [13573]
#tickerArray.pop(2)
#tickerArray.pop(1)
global time1
time1 = datetime.datetime.now() 
#n = get_list_multi(Tickers[0])
with Pool(400) as p:
    n.extend(p.map(get_list_multi, tickerArray))

time2 = datetime.datetime.now() 
elapsedTime = time2 - time1
elapsedTime
print(divmod(elapsedTime.total_seconds(), 60))
print(str(urlCount.value) + " URL opens")
print("Opens per second = " + str((urlCount.value/elapsedTime.total_seconds())))

p.close()
p.join()

toScrape = pd.DataFrame(n)
toScrape.to_pickle("./firstFunction.pkl")
toScrape.to_excel("toScrape.xlsx")

headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
            }


manager = Manager() 
m = manager.list()
q = []
with Pool(400) as p1:
    (p1.map(runScraper, n))

#print(q) 
#print(type(q))

p1.close()
p1.join()

#print(q)
#print(dir(q))
#data = pd.DataFrame(m)

#data.to_pickle("./secondFunction.pkl")



#data.to_excel("data.xlsx")
print(divmod(elapsedTime.total_seconds(), 60))
print(str(urlCount.value) + " URL opens")
print("Opens per second = " + str((urlCount.value/elapsedTime.total_seconds())))

























