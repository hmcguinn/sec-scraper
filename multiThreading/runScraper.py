#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import settings
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import lxml
import os
import datetime
from opensPerSecond import opensPerSecond
import traceback

def runScraper(array): 
    global urlCount
    global m 
    headers = {
                   'Access-Control-Allow-Origin': '*',
                   'Access-Control-Allow-Methods': 'GET',
                   'Access-Control-Allow-Headers': 'Content-Type',
                   'Access-Control-Max-Age': '3600',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
                   }
    
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
            with settings.urlCount.get_lock():
                settings.urlCount.value += 1 
                #print(urlCount.value)
                opensPerSecond(settings.urlCount.value,settings.time1)

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
            with settings.urlCount.get_lock():
                settings.urlCount.value += 1 
                #print(urlCount.value)
                opensPerSecond(settings.urlCount.value,settings.time1)

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

