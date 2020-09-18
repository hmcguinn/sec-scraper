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
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
            }  
    href = []
    #global urlCount 
    #urlCount = 0
    try:
        cik = cik1
        print("cik is " + str(cik))
        base_url_part1 = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
        base_url_part2 = "&type=&dateb=&owner=only&start="
        base_url_part3 = "&count=100&output=xml"

        for page_number in range(0,100000,100):
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
        print("some exception occured" + " " + base_url)
        print(inst)
        pass

    return (href)

