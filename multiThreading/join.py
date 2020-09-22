#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os 
import pandas as pd 
import numpy as np
import glob





#all_data = pd.DataFrame()
masterList = [] 
for f in glob.glob("./data/*_data.xlsx"):
    df = pd.read_excel(f)
    #print(df.head())

    #print(df["issuerName"][0])
    length = len(df) 
    for i in range(length): 
        form4Object = {"issuerName": df["issuerName"][i], "issuerCik": df["issuerCik"][i], 
                             "individualName": df["individualName"][i],
                             "reporterCik": df["reporterCik"][i], "Director?": df["Director?"][i],
                             "Officer?": df["Officer?"][i], "Ten Percent?": df["Ten Percent?"][i],
                             "Other?": df["Other?"][i], "Title": df["Title"][i], "Date": df["Date"][i],
                             "Form": df["Form"][i], "URL": df["URL"][i]}
        masterList.append(form4Object)
    
    

#print(all_data.describe())
all_data = pd.DataFrame(masterList)
all_data.to_excel("./joined_data.xlsx")
