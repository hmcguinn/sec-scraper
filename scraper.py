#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas 
import re


"""
Parameters: 
    rawInput    -------- raw XML file from SEC site
    searchField -------- search field we want to extract from 
Returns: 
    titleString -------- string with desired field 
Example: 
    rawInput    -------- <officerTitle>Chief Executive Officer</officerTitle>
    searchField -------- officerTitle
    titleString -------- Chief Executive Officer
"""
def getField(rawInput, searchField): 
    searchString = "<" + searchField + ">(.+)<\/" + searchField + ">" 
    title = re.search(searchString, rawInput)
    titleString = title.group(1)
    return titleString 


string = "<officerTitle>ChiefExecutiveOfficer</officerTitle>"
print(getField(string, "officerTitle"))
string = "<officerTitle>CFO</officerTitle>"

print(getField(string, "officerTitle"))
string = "<officerTitle>CFO & Vice</officerTitle>"

print(getField(string, "officerTitle"))
string = "<officerTitle>CFO & Vice12 asdn 12e </officerTitle>"

print(getField(string, "officerTitle"))
