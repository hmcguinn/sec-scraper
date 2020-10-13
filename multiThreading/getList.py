#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
from bs4 import BeautifulSoup
import lxml
from opensPerSecond import opensPerSecond
import traceback
import settings 

def get_list_multi(cik1):
    global urlCount
    headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3000',
            'Accept-Language': 'en-gb',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.11.1 Safari/605.1.15'
            }  
    href = []
    #global urlCount 
    #urlCount = 0
    retries = 0 
    try:
        cik = cik1
        print("cik is " + str(cik))
        base_url_part1 = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
        base_url_part2 = "&type=&dateb=&owner=only&start="
        base_url_part3 = "&count=100&output=xml"

        c = True
        page_number = 0
        #for page_number in range(0,100000,100):
        while c:
            tryScrape = True
            if retries > 100: 
                print("<<<<<<<<<<<<<<<<<<<<<<<<<<< MAX RETRIED FAILED >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                break
            if page_number == 1900: 
                page_number = 0     
                base_url_part2 = "&type=&dateb=" + str(report_year) + "0101" + "&owner=only&start="
                continue 
            base_url = base_url_part1 + str(cik) + base_url_part2 + str(page_number) + base_url_part3
            
            #print(page_number) 
            print(base_url)
            with settings.urlCount.get_lock():
                settings.urlCount.value += 1 
                #print(urlCount.value)
                opensPerSecond(settings.urlCount.value,settings.time1)

            #sec_page = url.urlopen(base_url)
            req = requests.get(base_url, headers)
            sec_soup = BeautifulSoup(req.content, "lxml")
            #print(sec_soup.prettify())
            
            
            head = sec_soup.findAll('h1')
            for h in head: 
                print(h.string)
                if h.string == "Service Unavailable": 
                    print("SERVICE UNAVAIALBLE ----------- ")  
                    time.sleep(10)
                    tryScrape = False
                    retries += 1 
                    continue
            if tryScrape: 
                filings = sec_soup.findAll('filing')
                if(len(filings)==0): 
                    c = False
                    print("LENGTH OF FILINGS WAS 0 BREAKING")
                    #break
                report_year = "" 
                for filing in filings:
                    #print(filing)
                    #time.sleep(.05)
                    report_year = int(filing.datefiled.get_text()[0:4])
                    if report_year < 2005: 
                        print("FIREST REPORT YEAR WAS BAD")
                        c = False
                        break
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
                page_number += 100
                if report_year < 2005: 
                    print("REPORT YEAR WAS BAD BREAKING")
                    c = False
                    break 
            
    except Exception as inst: 
        print("some exception occured" + " " + base_url)
        print(inst)
        pass

    return (href)

