#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd 
import re
import requests
import time 
import urllib.request as url 
from bs4 import BeautifulSoup

def get_list(cik):

        base_url_part1 = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
        base_url_part2 = "&type=&dateb=&owner=&start="
        base_url_part3 = "&count=100&output=xml"
        href = []
                        
        for page_number in range(0,2000,100):
        
            base_url = base_url_part1 + cik + base_url_part2 + str(page_number) + base_url_part3
                       
            sec_page = url.urlopen(base_url)
            sec_soup = BeautifulSoup(sec_page, "lxml")
                                    
            filings = sec_soup.findAll('filing')
                                                
            for filing in filings:
                
                time.sleep(.1) 
                report_year = int(filing.datefiled.get_text()[0:4])
                if (filing.type.get_text() == "4" or filing.type.get_text() == "3") & (report_year >= 2005):
                    print(filing.filinghref.get_text())
                    href.append(filing.filinghref.get_text())
            break
        time.sleep(.1) 
        return (href)
        



## import csv CIKS 
## loop through each one 

array = get_list("320193")
rows = [] 
headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
count = 0
for x in array: 
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

    count = count +1 
    print(count)
    exampleURL = x 

    req = requests.get(exampleURL, headers)
    soup1 = BeautifulSoup(req.content, 'xml')
    #print(exampleURL)
    s = None 
    #print(soup1.prettify())
    for link in soup1.find_all('a'): 
        
        #print(link.text)
        pattern = re.compile(r'wf-form\d_\d+\.xml')
        if(pattern.match(link.text)): 
            r = re.search('wf-form\d_\d+\.xml',link.text)
            if(r.group()): 
                #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + link.text)
                newLink = r.string 
                break 
        
    x = exampleURL.split("/") 
    
    for i in range(0,len(x)-1):
        if(s): 
            s = s + "/" + x[i]
            #print(s)
        else: 
            s = x[i]
    s =   s + "/" + newLink
    s.lstrip("/")
    #print("final s is " + s)
    req2 = requests.get(s, headers)
    soup = BeautifulSoup(req2.content, 'xml')
          
    #print(exampleURL)

    individualName = soup.rptOwnerName.string
    individualName = individualName.title()
    issuerName = soup.issuerName.string
    issuerCik = soup.issuerCik.string
    issuerCik = issuerCik.lstrip("0")
    date = soup.periodOfReport.string


    isDirector = soup.isDirector.string
    if(isDirector == '1'): 
        isDirector = "Yes"
    else: 
        isDirector = "No"

    isOfficer = soup.isOfficer.string
    if(isOfficer == '1'): 
        isOfficer = "Yes"
    else: 
        isOfficer = "No" 
 
    isTenPercentOwner = soup.isTenPercentOwner.string
    if(isTenPercentOwner == '1'): 
        isTenPercentOwner = "Yes"
    else: 
        isTenPercentOwner = "No"

    isOther = soup.isOther.string
    if(isOther == '1'): 
        isOther = "Yes"
    else: 
        isOther = "No" 


    reporterTitle= soup.officerTitle.string
    reporterCik = soup.rptOwnerCik.string
    reporterCik = reporterCik.lstrip("0")
    documentType = soup.documentType.string

    form4Object = {"issuerName": issuerName, "issuerCik": issuerCik, "individualName": individualName, 
                   "reporterCik": reporterCik, "Director?": isDirector, 
                   "Officer?": isOfficer, "Ten Percent?": isTenPercentOwner, 
                   "Other?": isOther, "Title": reporterTitle, "Date": date, 
                   "Form": documentType}  
    rows.append(form4Object)



df = pd.DataFrame(rows)
df.to_excel("test1.xlsx")
#df.rename(columns={"one"})
print(df.head)
print()
print()
print()
print()
print()
print(df)
#print(form4Object)


#print(issuerName)
#print(issuerCik)
#print(date)
#print(individualName)
#print(reporterCik)
#print(isDirector)
#print(isOfficer)
#print(isTenPercentOwner)
#print(isOther)
#print(reporterTitle)





#### beautiful soup tings to grab data  
#### soup object for one 









