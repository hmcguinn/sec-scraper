#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os 
import pandas as pd 
import numpy as np
import glob


validationData = pd.read_excel("validate_last.xlsx") 
validateAmount= validationData['Filings'].tolist()
company = validationData['CIK'].tolist()

newSet = {} 

difference = 0 
missing = 0 
zero = 0
print("Company \t Actual \t Expected \t 3A \t\t 4A \t\t Diff \t\t Norm")
results = [] 
for i in range(len(company)):
    try: 
        fileName = "./data/" + str(company[i]) + "_data.xlsx"
        companyData = pd.read_excel(fileName) 
        x = companyData['issuerName'].tolist()
        formCount = companyData['Form'].tolist() 
        threeACount = formCount.count("3/A")
        fourACount= formCount.count("4/A")
        difference += abs(len(x)-int(validateAmount[i]))
        entryObj = { 
                    "Company": company[i], 
                    "Actual": len(x), 
                    "Expected": validateAmount[i], 
                    "3A": threeACount, 
                    "4A": fourACount, 
                    "Diff": (len(x)-int(validateAmount[i])) 
        
                }
        results.append(entryObj)
        print(str(company[i]) + "\t\t" + str(len(x)) + "\t\t" + str(validateAmount[i]) + 
              "\t\t" + str(threeACount) + "\t\t" + str(fourACount) + 
              "\t\t" + str(len(x)-int(validateAmount[i])) 
              )
                
       
    except Exception as e:  
        missing += 1  
        print(str(company[i]) + "\t\t" + "N/A" + "\t\t" + str(validateAmount[i]) + "\t\t" + "N/A")
        try: 
            if int(validateAmount[i]) == 0: 
                zero += 1 
        except: 
            pass


print(difference)
print(difference/len(company))
df = pd.DataFrame(results)
df.to_excel("validateExcel.xlsx")
print(missing)
print(len(company))
print(zero)
